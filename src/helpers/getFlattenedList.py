def getFlattenedList(arrays):
    flattened_list = [item for sublist in arrays for inner in sublist for item in (inner if isinstance(inner, list) else [inner])]

    return ' '.join(flattened_list)

def array_to_string(data):
    if isinstance(data, list):
        return '[' + ', '.join(array_to_string(item) for item in data) + ']'
    return str(data)