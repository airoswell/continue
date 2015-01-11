# Models and serializers
from app.serializers import *
from app.errors import *
# Django Core
from django.core.exceptions import FieldError
# Django Rest Framework
from rest_framework.response import Response
from rest_framework import status as st
# Other Python module


class Crud:

    def __init__(self, user, model):
        self.model = model
        self.user = user        # For record-level permissions purpose
        self.errors = []
        self.status = st.HTTP_200_OK

    def get(self, **kwargs):
        try:
            insatnce = self.model.objects.get(**kwargs)
            return insatnce
        except model.DoesNotExist, e:
            errors = [e.message]
            return None, errors

    def create(self, validated_data, *args, **kwargs):
        try:
            queryset = self.model.create(validated_data, *args, **kwargs)
        except FieldError, e:
            self.status = st.HTTP_400_BAD_REQUEST
            print("\t\tCRUD.create FieldError ========>")
            print("\t\t\t %s" % (e.message))
            return
        return queryset

    def retrieve(self, page, items_per_page, **search_kwargs):
        start = (page - 1) * items_per_page
        end = page * items_per_page
        queryset = (self.model.objects.filter(**search_kwargs)
                    .order_by('-pk')[start: end])
        if not queryset:
            self.status = st.HTTP_404_NOT_FOUND
        return queryset

    def update(self, validated_data, *args, **kwargs):
        """
        Return:
        - instance
        """
        try:
            instance, errors = self.model.update(validated_data, **kwargs)
            print "\t\t CRUD.update ==> errors %s" % (errors)
            return instance
        except:
            return False

    def delete(self):
        return


def retrieve_records(model, serializer, page, items_per_page, **search_kwargs):
    """
        Retrieve records.
        Return:
        - (a list of serialized data, status), if records are found,
        - (empty list, if no record is found, status),
        - (error object, status)
    """
    start = (page - 1) * items_per_page
    end = page * items_per_page
    queryset = (model.objects.filter(**search_kwargs)
                .order_by('-pk')[start: end]
                )
    # ================================================================
    # Deal with serialization errors
    try:
        serialized = serializer(queryset, many=True)
        serialized.data     # Call once to detect potential FieldError
    except FieldError:
        return ({"error": "Incorrect query kwargs.",
                 "error_detail": "Ask the administrator."},
                st.HTTP_400_BAD_REQUEST)
    except KeyError:
        queryset = ErrorHandler(serializer).key_error_filter(queryset)
    # ================================================================
    serialized = serializer(queryset, many=True)
    status = st.HTTP_200_OK if queryset else st.HTTP_404_NOT_FOUND
    return serialized.data, status


def retrieve_a_record(model, model_serializer, **search_kwargs):
    data, status = retrieve_records(
        model, model_serializer,
        page=1, items_per_page=1,
        **search_kwargs)
    if status is st.HTTP_200_OK and data:
        data = data[0]
    return data, status


def retrieve_an_instance(model, **search_kwargs):
    try:
        return model.objects.get(**search_kwargs), st.HTTP_200_OK
    except model.DoesNotExist:
        return None, st.HTTP_404_NOT_FOUND


def run_and_respond(op, model, model_serializer, *args, **search_kwargs):
    """
    A shortcut function, typically for quick GET request.
    For post, put and delete, use the individual operational function
    (create_a_record, update_a_record, etc.) above instead.
    """
    data, status = op(model, model_serializer, *args, **search_kwargs)
    return Response(status=status, data=data)