"""Functions for managing categorical fields"""

def table_encode(encodings):
    """Encode fields in table
    
    For the moment we support only extended missing values specified in the
    encodings.
    """
    
    convert_dict = {}
    missing_vals = {}
    for var in encodings:
        convert_dict[var] = {y: x for x, y in encodings[var].items()}
        missing_vals[var] = [x for x in encodings[var] if isinstance(x, str)]
    
    def step(resource):
        
        current = resource.to_copy()
        encoded = [index for index, field in enumerate(current.schema['fields'])
                   if field['name'] in encodings]
        
        # Data
        def data():
            table = current.to_petl()
            return table.convert(convert_dict)
        
        # Meta
        resource.data = data
        for field in encoded:
            name = resource.schema['fields'][field]['name']
            resource.schema['fields'][field]['type'] = 'any'
            resource.schema['fields'][field]['encoding'] = encodings[name]
            if 'missingValues' in resource.schema['fields'][field]:
                resource.schema['fields'][field]['missingValues'] = \
                    resource.schema['fields'][field]['missingValues'] + \
                    missing_vals[name]
            else:
                resource.schema['fields'][field]['missingValues'] = missing_vals[name]
    
    return step
