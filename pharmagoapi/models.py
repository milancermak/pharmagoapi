from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model

from . import utils

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=utils.now_with_tz)
    updated_at = models.DateTimeField(default=utils.now_with_tz)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}(id={!r})".format(self.__class__.__name__, self.pk)

    def save(self, *args, **kwargs):
        self.updated_at = utils.now_with_tz()
        super().save(*args, **kwargs)


class Customer(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)

    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def get_absolute_url(self):
        return "/api/cigars/%i/" % self.id

    @property
    def customer_id(self):
        return self.pk


class Residence(BaseModel):
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)

    customer = models.OneToOneField(
        "Customer", on_delete=models.CASCADE, primary_key=True
    )


class Prescription(BaseModel):
    medicine_name = models.CharField(max_length=50, blank=True, null=True)
    medicine_description = models.CharField(max_length=254, blank=True, null=True)
    dosage_description = models.CharField(max_length=254, blank=True, null=True)

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    @property
    def prescription_id(self):
        return self.pk

