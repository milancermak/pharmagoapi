from __future__ import annotations

from rest_framework import decorators, mixins, parsers, response, status, viewsets
from rest_framework.reverse import reverse

from . import utils

class OwnerFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerSaveMixin:
    def perform_create(self, serializer):
        serializer.save(**self.get_serializer_save_kwargs())

    def get_serializer_save_kwargs(self):
        kwargs = dict(owner=self.request.user)
        if "HTTP_BS_SESSION_ID" in self.request.META:
            session, is_created = commonmodels.Session.objects.get_or_create(
                session_id=self.request.META["HTTP_BS_SESSION_ID"]
            )
            kwargs["session"] = session
        return kwargs


class ListModelMixin:
    # Equivalent to ListModelMixin.list()
    def custom_list(self, request, queryset, serializer_class, filterset_class=None):
        try:
            queryset = queryset.order_by("pk")
            if filterset_class is not None:
                filterset = filterset_class(
                    data=request.GET, request=request, queryset=queryset
                )
                if not filterset.is_bound or filterset.is_valid():
                    queryset = filterset.qs
                else:
                    queryset = filterset.queryset.none()

            page = self.paginate_queryset(queryset.all())
            if page is not None:
                serializer = serializer_class(
                    page, many=True, context=dict(request=request)
                )
                resp = self.get_paginated_response(serializer.data)
            else:
                serializer = serializer_class(
                    queryset, many=True, context=dict(request=request)
                )
                resp = response.Response(serializer.data)

            resp["X-Total-Count"] = queryset.count()
            return resp
        except exceptions.ValidationError as exc:
            return response.Response(data=exc, status=status.HTTP_400_BAD_REQUEST)

class ChildMixin(ListModelMixin):
    _child_object = None

    def get_child_object(self):
        return self._child_object

    def child_perform_create(self, serializer, parent_name, parent):
        kwargs = self.get_serializer_save_kwargs()
        kwargs[parent_name] = parent
        self._child_object = serializer.save(**kwargs)
        return self._child_object

    def child_action(
        self,
        request,
        serializer_class,
        queryset,
        view_name,
        lookup_field,
        parent_name,
        filterset_class=None,
    ):
        if request.method == "GET":
            return self.custom_list(
                request, queryset, serializer_class, filterset_class
            )
        elif request.method == "POST":
            # Equivalent to CreateModelMixin.create()
            parent = self.get_object()

            serializer = serializer_class(
                data=request.data, context=dict(request=request, parent=parent)
            )
            serializer.is_valid(raise_exception=True)

            self.child_perform_create(serializer, parent_name, parent)

            headers = (
                {
                    "Location": utils.build_absolute_url(
                        path=reverse(
                            view_name,
                            args=[getattr(self.get_child_object(), lookup_field)],
                        )
                    )
                }
                if view_name is not None
                else {}
            )

            return response.Response(
                serializer.data, headers=headers, status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)