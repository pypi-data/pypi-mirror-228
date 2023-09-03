"""Utilities for manipulating data from a REDCap project"""

from dataforge.sources.redcap.schema import schema
from dataforge.sources.redcap.transforms import transform_data
from collections import OrderedDict
import numpy as np
import pandas as pd
import glob
import os
import re
import sys
import html

class REDCapProject:
    """Inspect and manipulate metadata and data from a REDCap project"""
    
    def __init__(self, project_name='', path='tmp/redcap'):
        
        last_export = self._last_export(project_name, path)
        if not last_export:
            raise Exception('No REDCap exports found')
        if project_name:
            project_name = project_name + '_'
        base = os.path.join(path, project_name)
        
        try:
            datafile = f'{base}DATA_LABELS_{last_export}.csv'
            # We use the Python engine here because it handles embedded newlines
            self.raw_data = pd.read_csv(datafile, engine='python',
                                        dtype='object', keep_default_na=False)
        except FileNotFoundError:
            print(f'Error reading REDCap data file: {datafile}')
            raise
        
        try:
            metafile = f'{base}{last_export}.REDCap.xml'
            with open(metafile) as f:
                metadata = schema.parse(f.read()).studies[0]
        except FileNotFoundError:
            print(f'Error reading REDCap metadata file: {metafile}')
            raise
        
        self.global_vars = metadata.global_variableses[0]
        self.metadata = metadata.meta_data_versions[0]
        self.record_id = self.metadata.redcap_record_id_field
        self.events = self._get_events()
        self.forms = self._get_forms()
    
    def _last_export(self, project_name, path):
        """Return datetime of last REDCap export"""
        
        if project_name:
            project_name = project_name + '_'
        files = sorted(glob.glob(f'{os.path.join(path, project_name)}*'))
        if files:
            s = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{4})\.csv$', files[-1])
            if s:
                return s.group(1)
    
    def _get_items(self):
        """Return dicionary of items indexed by OID"""
        
        items = {}
        for item_def in self.metadata.item_defs:
            items[item_def.oid] = REDCapItem(item_def)
        return items
    
    def _get_item_groups(self):
        """Return dicionary of item groups indexed by OID"""
        
        items = self._get_items()
        item_groups = {}
        for item_group_def in self.metadata.item_group_defs:
            item_groups[item_group_def.oid] = []
            for item_ref in item_group_def.item_refs:
                item_groups[item_group_def.oid].append(items[item_ref.item_oid])
        return item_groups
    
    def _get_events(self):
        """Return dictionary of events indexed by REDCap unique event name
        
        Will be empty for non-longitudinal studies.
        """
        
        events = {}
        for study_event_def in self.metadata.study_event_defs:
            event = REDCapEvent(study_event_def, self.global_vars
                                .redcap_repeating_instruments_and_eventses)
            events[study_event_def.redcap_unique_event_name] = event
        return events
    
    def _get_forms(self):
        """Return dictionary of all forms indexed by form name"""
        
        forms = {}
        item_groups = self._get_item_groups()
        
        try:
            repeating_instruments = (self.global_vars.redcap_repeating_instruments_and_eventses[0]
                                     .redcap_repeating_instrumentses)
        except (IndexError):
            repeating_instruments = []
        
        for form_def in self.metadata.form_defs:
            repeat_events = {}
            for instruments in repeating_instruments:
                for instrument in instruments.redcap_repeating_instruments:
                    label = instrument.redcap_custom_label[1:-1]
                    if instrument.redcap_repeat_instrument==form_def.redcap_form_name:
                        repeat_events[instrument.redcap_unique_event_name] = label
            
            forms[form_def.name] = REDCapForm(self, form_def, item_groups,
                                              self.events, repeat_events)
        return forms
    
    def _merge_data(self, form_data):
        """Merge data from multiple forms"""
        
        dag = 'redcap_data_access_group'
        repeated_forms = False
        for form, data in form_data.items():
            
            # Add DAG to index temporarily to facilitate merging
            if dag in data:
                data.set_index(dag, append=True, inplace=True)
            
            if self.forms[form].repeat:
                if not repeated_forms:
                    repeated_forms = True
                else:
                    raise Exception('Multiple repeated forms not supported')
            
            try:
                df = df.merge(data, how='outer', left_index=True,
                              right_index=True, sort=True)
            except UnboundLocalError:
                df = data
        
        # Remove from index after merging
        if dag in df.index.names:
            df.insert(0, dag, df.index.get_level_values(dag).values)
            df = df.droplevel(dag)
        
        return df.sort_index()
    
    def data(self, forms=None, dag='data_access_group', **kwargs):
        """Return data for one or more forms/instruments
        
        forms: List containing forms from which to return data
          dag: Name for column containing DAG, or False/None to exclude
        """
        
        if forms is None:
            forms = self.forms.keys()
        
        form_data = OrderedDict()
        for form in forms:
            form_data[form] = self.forms[form]._get_data(**kwargs)
        
        df = self._merge_data(form_data)
        
        if 'redcap_data_access_group' in df:
            if dag:
                df.rename(columns={'redcap_data_access_group':dag}, inplace=True)
            else:
                df.drop(columns=['redcap_data_access_group'], inplace=True)
        
        return df
    
    def missing_report(self, forms=None):
        """Return boolean dataframe indicating whether items are missing
        
        Takes into account branching logic. Should include option to ignore
        fields marked as not required.
        
        Implementation idea (inefficient but provides straightforward way to
        handle all cases):
        
        Collect data from *all* project forms, and place in EAV format (i.e.,
        multi-key dictionary). For each form in argument forms, go through
        each item. If item does not have branching logic, set empty strings to
        missing. If item does have branching logic, use apply() with a
        callable to set missing values. Callable would evaluate branching
        logic by interpreting REDCap's DSL and, for each record, replacing
        values of variable(s) in expression using EAV dictionary.
        """
        
        raise NotImplementedError

class REDCapEvent:
    
    def __init__(self, study_event_def, repeating_instruments_and_events):
        
        self.name = study_event_def.name
        self.unique_name = study_event_def.redcap_unique_event_name
        self.forms = set()
        for form_ref in study_event_def.form_refs:
            self.forms.add(form_ref.form_oid)
        
        self.repeat = False
        if repeating_instruments_and_events:
            for event in repeating_instruments_and_events[0].redcap_repeating_events:
                if event.redcap_unique_event_name==self.unique_name:
                    self.repeat = True
                    break

class REDCapForm:
    """A REDCap form
    
    Note that we intentionally collapse over item groups when creating the
    list of items, since the metadata lost (i.e., sections and matrices) is
    not typically necessary for creating data products and the result is
    considerably simpler.
    
    Repeat events is a dictionary indexed by the events within which the form
    repeats, with the entries containing the variable used to index individual
    instances of the form.
    """
    
    def __init__(self, project, form_def, item_groups, events, repeat_events):
        self.project = project
        self.name = form_def.name
        self.form_name = form_def.redcap_form_name
        self.items = []
        for item_group_ref in form_def.item_group_refs:
            self.items.extend(item_groups[item_group_ref.item_group_oid])
        self.events = []
        for event in events:
            if form_def.oid in events[event].forms:
                self.events.append(events[event])
        self.repeat = repeat_events
    
    def _reindex(self, df):
        """Reindex dataframe exported from REDCap for easier use
        
        Resulting index: record_id, [arm,] [event,] [event_instance,] [form_instance,]
        
        We handle the following cases:
        
        1. No events (record_id)
        2. No events, repeating form (record_id, form_instance)
        3. Form in one non-repeating event (record_id [,arm] [,form_instance])
        4. Form in repeating event (record_id, [arm,] event, event_instance)
        5. Form in multiple events, form not repeating (record_id, [arm,] event [, event_instance])
        6. Form in multiple events, repeating form (record_id, [arm,] event, [event_instance,] form_instance)
        
        Although we might consider an option to permit using REDCap custom
        labels as indices for repeated events and forms (i.e., event_instance
        and form_instance), this might result in a non-unique index. Moreover,
        it is possible for the datatypes of these labels to vary across
        events, depending on how they are configured in REDCap.
        """
        
        idx = [self.project.record_id]
        if 'redcap_event_name' in df.columns:
            
            # Handle multiple arms; always include arm if present, since same
            # record ID may appear in multiple arms
            if df.redcap_event_name.str.contains(r' \(Arm [0-9]+').any():
                arm = df.redcap_event_name.str.extract(r' \((Arm [0-9]+.+)\)').iloc[:,0]
                idx.append(arm.rename('arm'))
                event = df.redcap_event_name.str.replace(r' \((Arm [0-9]+.+)\)',
                                                         '', regex=True).\
                                                 rename('event')
            else:
                event = df.redcap_event_name.rename('event')
            
            if (len(self.events) > 1):
                idx.append(event)
        
        # Split instance variable to create more intuitive and usable result
        if [e for e in self.events if e.repeat]:
            if idx[-1] is not event:
                idx.append(event)
            
            if 'redcap_repeat_instrument' in df:
                event_instance = df.redcap_repeat_instance.\
                                 where(df.redcap_repeat_instrument=='', '')
            else:
                event_instance = df.redcap_repeat_instance
            
            idx.append(event_instance.rename('event_instance'))
        
        if self.repeat:
            form_instance = df.redcap_repeat_instance.\
                            where(df.redcap_repeat_instrument==self.name, '')
            idx.append(form_instance.rename('form_instance'))
        
        df.set_index(idx, append=False, inplace=True, verify_integrity=True)
    
    def _get_data(self, **kwargs):
        """Return data frame containing form data
        
        We rely in part on the exported dataset for information about arms,
        repeating events and repeating forms. Although we could also get that
        information from the metadata, doing so wouldn't necessarily result in
        simpler code. Moreover, if REDCap ever changes the way in which it
        represents this information in the dataset, we'll have to update the
        code regardless.
        """
        
        # Drop records not containing data for this form
        data = self.project.raw_data.copy()
        if 'redcap_event_name' in data.columns:
            event_names = [e.name for e in self.events]
            data = data.loc[data['redcap_event_name'].isin(event_names)]
        if 'redcap_repeat_instrument' in data:
            data = data.loc[data.redcap_repeat_instrument.isin([self.name,''])]
        
        self._reindex(data)
        
        # Return fields on form only
        keep = (['redcap_data_access_group']
                if 'redcap_data_access_group' in data else [])
        keep.extend([item.oid for item in self.items if item.oid in data.columns])
        data = data[keep]
        
        # Drop empty rows
        data = data.replace(r'^\s*$', np.NaN, regex=True).dropna(how='all')
        
        transform_data(self, data, **kwargs)
        return data.sort_index()

class REDCapItem:
    
    def __init__(self, item_def):
        
        self.oid = item_def.oid
        self.name = item_def.name
        self.data_type = item_def.data_type
        self.length = item_def.length
        self.varname = item_def.redcap_variable
        self.field_type = item_def.redcap_field_type
        self.text_validation_type = item_def.redcap_text_validation_type
        if item_def.redcap_required_field=='y':
            self.required = True
        else:
            self.required = False
        if item_def.redcap_branching_logic:
            self.branching_logic = html.unescape(item_def.redcap_branching_logic)
        else:
            self.branching_logic = None
        self.question = item_def.questions[0].translated_texts[0]
