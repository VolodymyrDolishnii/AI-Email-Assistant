def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, list):
        return [convert_bytes_to_str(item) for item in data]
    return data