"""
This file is used for formatting (serializing) data interacting with the generated models.
"""
from rest_framework import serializers
from .models import PurchaseInfoModel


class PurchaseInfoModelSerializer(serializers.ModelSerializer):
    """
    Class for defining how project creation request and response object should look like.
    """
    class Meta:
        model = PurchaseInfoModel
        fields = '__all__'
