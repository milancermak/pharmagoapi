from __future__ import annotations

from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication,
    JSONWebTokenAuthentication,
)
from rest_framework import exceptions

class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        try:
            user_token_tuple = super().authenticate(request)
        except exceptions.APIException as e:
            try:
                user_token_tuple = JSONWebTokenAuthentication().authenticate(request)
            except Exception:
                raise e
        return user_token_tuple