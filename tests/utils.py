def run_is_valid(serializer_class, data):
    instance = serializer_class(data=data)
    instance.is_valid()
    return instance
