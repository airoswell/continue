class ErrorHandler:

    def __init__(self, serializer):
        self.serializer = serializer
        self.status = None
        self.errors = {}

    def validate(self, data):
        """
        <data> should be request.data, clean it up (through away invalid data)
        and it will
        be altered after the process due to

        Return:
        - <data> (filtered version)
        """
        data_serialized = self.serializer(data=data)
        if data_serialized.is_valid():
            return data_serialized.validated_data
        self.errors = data_serialized.errors
        print("\n\t !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("\t\nErrorHandler.validate() ==> %s" % (self.errors))
        print("\n\t !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for field in data_serialized.errors:
            for msg in data_serialized.errors[field]:
                if msg != "This field may not be blank.":
                    data.pop(field)
                    self.errors[field] = msg
                else:
                    self.errors["fatal"] = data_serialized.errors
        return data

    def key_error_filter(self, queryset):
        """
        Filter out invalid instances that cannot be serialized
        in a queryset.

        Return:
        - A filtered queryset without KeyError
        """
        valid_instances = []
        for instance in queryset:
            serialized = self.serializer(instance)
            try:
                serialized.data
                valid_instances.append(instance)
            except KeyError:
                pass
        return valid_instances
