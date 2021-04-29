from __future__ import annotations

from django.shortcuts import render

from rest_framework import decorators, mixins, response, status, viewsets, views

from . import models
from . import serializers
from . import baseviews


class CustomerViewSet(viewsets.ModelViewSet, baseviews.ChildMixin, baseviews.OwnerSaveMixin, baseviews.OwnerFilterMixin):
    queryset = models.Customer.objects.order_by("pk").all()
    serializer_class = serializers.CustomerSerializer

    def get_prescription_serializer_class(self):
        return serializers.PrescriptionSerializer

    def get_prescription_model_class(self):
        return models.Prescription

    @decorators.action(detail=True, methods=["get", "post"])
    def prescriptions(self, request, pk):
        return self.child_action(
            request,
            serializer_class=self.get_prescription_serializer_class(),
            view_name="prescription-detail",
            queryset=self.get_object().prescription_set.all(),
            lookup_field="pk",
            parent_name="customer",
        )


class PrescriptionViewSet(
    baseviews.OwnerSaveMixin,
    baseviews.OwnerFilterMixin,
    viewsets.ModelViewSet
):

    queryset = models.Prescription.objects.all()
    serializer_class = serializers.PrescriptionSerializer


