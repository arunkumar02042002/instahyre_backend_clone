# Function that returns an error message realted to serializers
def validation_error_handler(data):

    # In serializers, more than one field can have errors
    key = list(data.keys())[0]
    value = data[key]

    # We can have more than one error with a field
    if type(value) is list:
        message = f'{key}: {value[0]}'
    else:
        message = f'{key}: {value}'
    return message