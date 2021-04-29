from __future__ import annotations

from django.db import transaction

from rest_framework import serializers

from . import models


class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Residence
        fields = [
            "address",
            "city",
            "zipcode",
        ]

class CustomerSerializer(serializers.ModelSerializer):
    residence = ResidenceSerializer()

    class Meta:
        model = models.Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "residence"
        ]
        read_only_fields = ["customer_id"]

    def create(self, validated_data):
        with transaction.atomic():
            residence_serializer = ResidenceSerializer(
                data=validated_data.pop("residence")
            )
            residence_serializer.is_valid(raise_exception=True)
            customer = super().create(validated_data)
            residence_serializer.save(customer=customer)

            return customer


class PrescriptionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        prescription = super().create(validated_data)
        return prescription

    class Meta:
        model = models.Prescription
        fields = [
            "medicine_name",
            "medicine_description",
            "dosage_description"
        ]
        read_only_fields = [
            "prescription_id"
        ]