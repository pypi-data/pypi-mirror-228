"""Transformations applied to data exported from a REDCap project"""

import numpy as np
import pandas as pd

def transform_data(form, data, status=False, rename_checkbox_fields=False):
    """Apply transforms to data in place"""
    
    strip_whitespace(data)
    translate_dates(form, data)
    
    if rename_checkbox_fields:
        rename_checkboxes(form, data)
    
    if not status:
        data.drop(columns=f'{form.form_name}_complete', inplace=True)

def strip_whitespace(df):
    """Strip leading/trailing whitespace and embedded newlines"""
    
    # Trim leading and trailing whitespace
    df.replace({r'^\s+':'', r'\s+$':''}, regex=True, inplace=True)
    
    # Remove embedded newlines
    df.replace(r'\r?\n', '  ', regex=True, inplace=True)

def translate_dates(form, df):
    """Translate date vars to datetime objects"""
    
    # REDCap exports all types in YYYY-MM-DD format
    types = ['date_dmy','date_mdy','date_ymd','datetime_dmy','datetime_mdy',
             'datetime_ymd','datetime_seconds_dmy','datetime_seconds_mdy',
             'datetime_seconds_ymd']
    
    for item in form.items:
        
        if item.text_validation_type in types:
            df[item.name] = pd.to_datetime(df[item.name], errors='coerce')
        
        elif item.text_validation_type=='date_my':
            incomplete = df[item.name].str.isnumeric()
            df[item.name] = pd.to_datetime(df[item.name],
                                           errors='coerce').dt.to_period('M')
            # Prevent coercion of just year (e.g., 2021 -> 2021-01)
            df[item.name] = df[item.name].where(incomplete!=True, np.NaN)

def rename_checkboxes(form, df):
    """Rename checkbox items to simplify"""
    
    map = {}
    for item in form.items:
        
        if item.field_type=='checkbox':
            
            varname = item.varname
            if len([c for c in df.columns if c.startswith(varname + '___')])>1:
                map[item.name] = varname + item.name[len(varname)+3:]
            else:
                map[item.name] = varname
    
    df.rename(columns=map, inplace=True)
