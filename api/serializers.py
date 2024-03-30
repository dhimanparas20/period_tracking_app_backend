from rest_framework import serializers
from .models import Period

class PeriodSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  
    class Meta:
        model = Period
        fields = '__all__'