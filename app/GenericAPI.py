from errors import ErrorHandler
from app.CRUD import *
from django.utils.six import BytesIO
# ======== Django Rest Framework ========
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework.parsers import JSONParser
# ================================
from controllers import *


class XListAPIView(APIView):

    def parser(self, request):
        data = request.data
        if "__copy__" in dir(request.data):
            data = request.data.items()[0][0]
            stream = BytesIO(data)
            data = JSONParser().parse(stream)
        return data

    def paginator(self, request):
        page = 1
        items_per_page = self.items_per_page
        params = request.query_params
        if "page" in params:
            page = int(params['page'])
        if "items_per_page" in params:
            items_per_page = int(params["items_per_page"])
        return page, items_per_page

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
            return Response(data=errors)
        except FieldDoesNotExist:
            # If the model does not have 'owner' field
            # pass in <user> to the model methods, let them decide
            instance, errors = crud.update(data, user=request.user)
        # ============================================================
        if instance:    # if the item is owned by the user
            data = self.serializer(instance).data
        else:
            return Response(data={
                "errors": """Unable to update the instance:
                crud.update(data, owner=request.user) does not return
                a instance.
                """
            })
        data['errors'] = errors
        status = crud.status
        return Response(data=data, status=status)
