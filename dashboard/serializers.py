"""
dashboard/serializers.py
"""

from rest_framework import serializers
from dashboard.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    UserSerializer
    """

    class Meta:
        model = Users
        fields = "__all__"
