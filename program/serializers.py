from rest_framework import serializers
from .models import Program, StudentAndProgram, ProgramCoordinatorAndProgram, CompanyRepresentativeAndProgram, \
    CompanyMentorAndProgram, ProgramManagerAndProgram


class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('program', 'department', 'year', 'semester', 'prioritiesAmount', 'hoursRequired', 'status')


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


# ProgramManagerAndProgramSerializers:
class ProgramManagerAndProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProgramManagerAndProgram
        fields = ('id', 'program_id', 'programManager_id')


# StudentAndProgramSerializers:
class StudentAndProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentAndProgram
        fields = ('id', 'program_id', 'student_id')


# ProgramCoordinatorAndProgramSerializers:
class ProgramCoordinatorAndProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProgramCoordinatorAndProgram
        fields = ('id', 'program_id', 'programCoordinator_id')


# CompanyRepresentativeAndProgramSerializers:
class CompanyRepresentativeAndProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyRepresentativeAndProgram
        fields = ('id', 'program_id', 'companyRepresentative_id')


# CompanyMentorAndProgramSerializers:
class CompanyMentorAndProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyMentorAndProgram
        fields = ('id', 'program_id', 'companyMentor_id')
