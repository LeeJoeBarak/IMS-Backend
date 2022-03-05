from rest_framework import serializers
from .models import Program


# class ProgramsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Program
#         fields = ('id', 'program', 'department', 'year', 'semester','programManager', 'programCoordinator', 'prioritiesAmount', 'hoursRequired')


class PrioritiesAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('program', 'prioritiesAmount')


class HoursRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('program', 'hoursRequired')
