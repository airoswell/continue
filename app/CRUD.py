# -*- coding: utf-8 -*-
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
            return insatnce, []
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
            return None
        return queryset

    def retrieve(self, start, num_of_records, **search_kwargs):
        end = start + num_of_records
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
        # instance, errors = self.model.update(validated_data, **kwargs)
        # print "\t\t CRUD.update ==> errors %s" % (errors)
        # return instance, errors
        try:
            print("\tCRUD.update()")
            instance, errors = self.model.update(validated_data, **kwargs)
            print("\t\t !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print "\t\t CRUD.update ==> errors %s" % (errors)
            print("\t\t !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return instance, errors
        except:
            return False, ["Unknown errors"]

    def delete(self):
        return


def retrieve_records(model, serializer, start, num_of_records, **search_kwargs):
    """
        Retrieve records.
        Return:
        - (a list of serialized data, status), if records are found,
        - (empty list, if no record is found, status),
        - (error object, status)
    """
    # start = (page - 1) * num_of_records
    # end = page * num_of_records
    end = start + num_of_records
    queryset = (model.objects.filter(**search_kwargs)
                .order_by('-pk')[start: end]
                )
    print("\n\tretrieve_records() returns queryset %s" % (queryset))
    # ================================================================
    # Deal with serialization errors
    try:
        serialized = serializer(queryset, many=True)
        print("\n\t serialized.data = %s" % (serialized.data))
        serialized.data     # Call once to detect potential FieldError
    except FieldError:
        return ({"error": "Incorrect query kwargs.",
                 "error_detail": "Ask the administrator."},
                st.HTTP_400_BAD_REQUEST)
    except KeyError, e:
        print("\n\t there is error in CRUD.retrieve_records: %s" % (e))
        queryset = ErrorHandler(serializer).key_error_filter(queryset)
        print("\n\t queryset = %s " % (queryset))
    # ================================================================
    serialized = serializer(queryset, many=True)
    status = st.HTTP_200_OK if queryset else st.HTTP_404_NOT_FOUND
    return serialized.data, status


def retrieve_a_record(model, model_serializer, **search_kwargs):
    data, status = retrieve_records(
        model, model_serializer,
        page=1, num_of_records=1,
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
