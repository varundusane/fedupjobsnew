from rest_framework import serializers
from .models import WorkDetails

class WorkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDetails
        fields = '__all__'
        depth =1
