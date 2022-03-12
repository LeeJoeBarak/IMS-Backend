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


class ProgramNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('program',)


class CreateProgramSerializer(serializers.ModelSerializer):
    # {
    #     "program": "string",
    #     "year": 0,
    #     "semester": "string",
    #     "prioritiesAmount": 0,
    #     "hoursRequired": 0,
    #     "depratment": "string",
    #     "programManager": "string"
    # }
    class Meta:
        model = Program
        fields = ('program', 'year', 'semester', 'prioritiesAmount', 'hoursRequired', 'department')

    def create(self, validated_data):
        program = Program.objects.create(
            program=validated_data['program'],
            year=validated_data['year'],
            semester=validated_data['semester'],
            prioritiesAmount=validated_data['prioritiesAmount'],
            hoursRequired=validated_data['hoursRequired'],
            department=validated_data['department']

        )
        return program
