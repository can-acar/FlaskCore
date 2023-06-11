import re

param_formats = {
    'alpha': '[a-zA-Z]+',
    'int': '[0-9]+',
    'float': '[0-9]*\.[0-9]+',
    'guid': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
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
    'any': '.+',
    'string': '[^/]+',
    'bool': 'true|false',
    'boolean': 'true|false',
    'regex': '[^/]+',
    'email': '[^/]+',
}


def create_regex(route):
    # Define regex patterns for different parameter types

    # Default format if no format is specified in the parameter
    default_format = '[^/]+'
    for param_format in param_formats:
        param_regex = param_formats[param_format]
        route = re.sub(r'\{(\w+):' + param_format + ':min\((\d+)\):max\((\d+)\)\}',
                       r'(?P<\1>' + param_regex + '{\2,\3})', route)

    # Replace {param:regex(regex rule)} with the corresponding regex pattern
    route = re.sub(r'\{(\w+):regex\(([^)]+)\)\}', r'(?P<\1>\2)', route)

    # Replace {param:type} with the corresponding regex pattern
    for param_format in param_formats:
        route = re.sub(r'\{(\w+):' + param_format + r'\}', r'(?P<\1>' + param_formats[param_format] + ')', route)

    # Replace remaining {param} occurrences with the default format
    route = re.sub(r'\{(\w+)\}', r'(?P<\1>' + default_format + ')', route)

    return route

# def create_regex(route):
#     route = route.replace("{", "(?P<")
#     route = route.replace("}", ">[^/]+)")
#     route = route.replace(":int", ":[0-9]+")
#     route = route.replace(":guid", ":[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
#     return re.compile(route)
# 'int': r'\d+',
# 'guid': r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
# 'any': r'[^/]+',
# 'alpha': r'[a-zA-Z]+',
# 'alphanum': r'[a-zA-Z0-9]+',
# 'path': r'.+',
# 'uuid': r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',
# 'slug': r'[a-z0-9]+(?:-[a-z0-9]+)*',
# 'short_slug': r'[a-z]+(?:-[a-z]+)*',
# 'float': r'[0-9]+(?:\.[0-9]+)?',
# 'decimal': r'[0-9]+(?:\.[0-9]+)?',
# 'date': r'\d{4}-\d{2}-\d{2}',
# 'datetime': r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
# 'time': r'\d{2}:\d{2}:\d{2}',
# 'email': r'[^@]+@[^@]+\.[^@]+',
# 'min(int)': r'\d+',
# 'max(int)': r'\d+',
#     route = re.sub(r'{(?P<param>[^:]+):(?P<format>[^}]+)}',
#                    lambda m: '(?P<{}>{})'.format(m.group('param'), route_param_formats.get(m.group('format'), '[^/]+')),
#                    route)
#     # route = re.sub(r'{(?P<param>[^}]+)}', r'(?P<\1>[^/]+)', route)
#     return re.compile(route)
