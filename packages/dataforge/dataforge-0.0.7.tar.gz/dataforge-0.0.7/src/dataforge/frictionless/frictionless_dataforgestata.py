"""Frictionless plugin providing Stata support

   Module named frictionless_dataforgestata instead of frictionless_stata to
   avoid confusion with possible future official Stata plugin.
"""

from frictionless import Parser, Control, Plugin, system
import pyreadstat
import re
import pandas as pd
import attrs

class StataParser(Parser):
    """Stata parser implementation"""

    supported_types = [
        'string',
    ]

    # Read

    def read_cell_stream_create(self):
        raise NotImplementedError('Reading Stata (.dta) files not yet implemented')

    # Write

    def __get_value_labels(self, source):
        
        value_labels = {}
        missing_vals = {}
        for field in source.schema.fields:
            if 'encoding' in field:
                missing = []
                encoding = field['encoding']
                for key in list(encoding):
                    if re.match('^\.[a-zA-Z]$', str(key)):
                        new_key = key.lower().replace('.', '')
                        encoding[new_key] = encoding.pop(key)
                        missing.append(new_key)
                value_labels[field['name']] = encoding
                if missing:
                    missing_vals[field['name']] = missing
        
        return value_labels, missing_vals

    def write_row_stream(self, source):
        
        value_labels, missing_vals = self.__get_value_labels(source)
        fields = [f['name'] for f in source.schema.fields]
        df = source.to_petl().todataframe()
        for field in missing_vals:
            df[field] = df[field].where(df[field].astype(str).str.isnumeric(),
                                        df[field].str.replace(r'^\.([a-zA-Z])$',
                                                              r'\1', regex=True))
        df = df.apply(pd.to_numeric, downcast='integer', errors='ignore')
        
        pyreadstat.write_dta(df, self.resource.path,
                             missing_user_values = missing_vals,
                             variable_value_labels = value_labels)

@attrs.define(kw_only=True)
class StataControl(Control):
    """Stata dialect representation"""

    type = 'stata'

class DataforgeStataPlugin(Plugin):
    """Plugin for Stata"""

    def create_parser(self, resource):
        if resource.format == 'dta':
            return StataParser(resource)

    def detect_resource(self, resource):
        if resource.format == 'dta':
            resource.type = 'table'

    def select_Control(self, type):
        if type == 'stata':
            return StataControl

system.register('dataforgestata', DataforgeStataPlugin())
