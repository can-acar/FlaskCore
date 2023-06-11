import re

param_formats = {
    'alpha': '[a-zA-Z]+',
    'int': '[0-9]+',
    'float': '[0-9]*\.[0-9]+',
    'guid': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
    'alphanum': '[a-zA-Z0-9]+',
    'path': '.+',
    'uuid': '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',
    'slug': '[a-z0-9]+(?:-[a-z0-9]+)*',
    'year': '[12][0-9]{3}',
    'month': '(?:0[1-9]|1[0-2])',
    'day': '(?:0[1-9]|[12][0-9]|3[01])',
    'date': '[12][0-9]{3}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])',
    'time': '(?:[01][0-9]|2[0-3]):[0-5][0-9]',
    'hour': '(?:[01][0-9]|2[0-3])',
    'minute': '[0-5][0-9]',
    'second': '[0-5][0-9]',
    'datetime': '[12][0-9]{3}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]',
    'file': '[^/]+',
    'any': '[^/]*',
    'string': '[^/]+',
    'bool': 'true|false',
    'boolean': 'true|false',
    'regex': '[^/]+',
    'email': '[^/]+',
    'min': '[0-9]{%s,}',
    'max': '[0-9]{0,%s}',
    'between': '[%s-%s]',
}


def create_regex(route):
    for match in re.finditer(r'\{(\w+?)(?::(\w+))?(?:\((.*?)\))?\??\}', route):
        param_name, param_type, param_value = match.groups()
        optional = match.group(0).endswith("?}")
        param_format = param_formats.get(param_type or 'any', '.+')

        if param_type in ['min', 'max', 'between']:
            values = map(int, param_value.split(","))
            param_format = param_format % tuple(values)
        elif param_type == 'regex':
            param_format = param_value

        if optional:
            param_format = f'(?:{param_format})?'

        route = route.replace(match.group(0), f'(?P<{param_name}>{param_format})')
    return route
