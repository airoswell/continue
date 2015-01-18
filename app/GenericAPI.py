from errors import ErrorHandler
from app.CRUD import *
from django.utils.six import BytesIO
# ======== Django Rest Framework ========
# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework.parsers import JSONParser
# ================================
import json


class XListAPIView(APIView):

    def parser(self, request):
        data = request.data
        if "__copy__" in dir(request.data):
            data = request.data.items()[0][0]
            data = json.loads(data)
        return data

    def paginator(self, request):
        # For single model query paginations
        start = 0
        num_of_records = self.num_of_records
        params = request.query_params
        if "start" in params:
            start = int(params['start'])
        if "num_of_records" in params:
            num_of_records = int(params["num_of_records"])
        if "page" in params:
            start = params * num_of_records
        return start, num_of_records

    def get_object(self, **search_kwargs):
        queryset = self.model.objects.filter(**search_kwargs)
        if queryset:
            for instance in queryset:
                self.check_object_permissions(self.request, instance)
        return queryset


class XDetailAPIView(APIView):
    def get_object(self, **search_kwargs):
        queryset = self.model.objects.filter(**search_kwargs)
        if queryset:
            instance = queryset[0]
            self.check_object_permissions(self.request, instance)
            return instance, st.HTTP_200_OK
        else:
            return None, st.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        instance, status = self.get_object(pk=pk)
        return Response(
            data=self.serializer(instance).data,
            status=status
        )

    def put(self, request, pk, format=None):
        # ============================================================
        # Data processing
        instance, status = self.get_object(pk=pk)  # Object permission purpose
        if status is st.HTTP_404_NOT_FOUND:
            return Response(data=instance, status=status)
        # Filter the data
        if hasattr(self, "deSerializer"):
            handler = ErrorHandler(self.deSerializer)
        else:
            handler = ErrorHandler(self.serializer)
        # return Response(data=request.data)
        data = handler.validate(request.data)
        errors = handler.errors
        data['id'] = pk         # If the data contains id, should preserve it
        # ============================================================
        # Perform update
        crud = Crud(request.user, self.model)
        from django.db.models.fields import FieldDoesNotExist
        try:
            # If the model has 'owner' field
            # only the object that is owned by the user can be updated
            self.model._meta.get_field("owner")
            instance, errors = crud.update(data, owner=request.user)
        except FieldDoesNotExist:
            # If the model does not have 'owner' field
            # pass in <user> to the model methods, let them decide
            print("\n\tdata = %s\n" % (data))
            instance, errors = crud.update(data, user=request.user)
        # ============================================================
        if instance:    # Update was successful
            data = self.serializer(instance).data
        else:           # Update failed
            return Response(data={
                "errors": """Unable to update the instance:
                crud.update(data, owner=request.user) does not return
                a instance.
                """
            })
        data['errors'] = errors
        status = crud.status
        return Response(data=data, status=status)
