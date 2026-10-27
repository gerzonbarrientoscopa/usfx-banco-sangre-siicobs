from __future__ import unicode_literals
import graphene
from graphene.types import generic
from graphql_jwt.decorators import permission_required

from sieves.models import ClinicalHistoryQuestion, ClinicalHistoryAnswer
from sieves.schema import ClinicalHistoryQuestionType, ClinicalHistoryAnswerType


class CreateClinicalHistoryQuestion(graphene.Mutation):
    clinicalhistoryquestion = graphene.Field(ClinicalHistoryQuestionType)

    class Arguments:
        title = graphene.String(required=True)
        register_at = graphene.Date()
        questions = generic.GenericScalar()
        is_active = graphene.Boolean(required=True)

    @permission_required(['sieves.add_clinicalhistoryquestion'])
    def mutate(self, info, title, is_active, **kwargs):
        clinicalhistoryquestion = ClinicalHistoryQuestion(title=title, is_active=is_active)

        if kwargs.get('questions', None) is not None:
            clinicalhistoryquestion.questions = kwargs.get('questions')
        if kwargs.get('register_at', None) is not None:
            clinicalhistoryquestion.register_at = kwargs.get('register_at')

        clinicalhistoryquestion.save()

        return CreateClinicalHistoryQuestion(clinicalhistoryquestion=clinicalhistoryquestion)


class UpdateClinicalHistoryQuestion(graphene.Mutation):
    clinicalhistoryquestion = graphene.Field(ClinicalHistoryQuestionType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        register_at = graphene.Date()
        questions = generic.GenericScalar()
        is_active = graphene.Boolean()

    @permission_required(['sieves.change_clinicalhistoryquestion'])
    def mutate(self, info, id, **kwargs):
        clinicalhistoryquestion = ClinicalHistoryQuestion.objects.filter(id=id).first()
        if clinicalhistoryquestion is None:
            raise ValueError('ClinicalHistoryQuestion not found')

        if kwargs.get('title', None) is not None:
            clinicalhistoryquestion.title = kwargs.get('title')
        if kwargs.get('is_active', None) is not None:
            clinicalhistoryquestion.is_active = kwargs.get('is_active')
        if kwargs.get('questions', None) is not None:
            clinicalhistoryquestion.questions = kwargs.get('questions')
        if kwargs.get('register_at', None) is not None:
            clinicalhistoryquestion.register_at = kwargs.get('register_at')

        clinicalhistoryquestion.save()

        return UpdateClinicalHistoryQuestion(clinicalhistoryquestion=clinicalhistoryquestion)


class CreateClinicalHistoryAnswer(graphene.Mutation):
    clinicalhistoryanswer = graphene.Field(ClinicalHistoryAnswerType)

    class Arguments:
        questionnaire_id = graphene.Int(required=True)
        donation_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        responses = generic.GenericScalar()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['sieves.add_clinicalhistoryanswer'])
    def mutate(self, info, questionnaire_id, donation_id, employee_id, register_id, **kwargs):
        clinicalhistoryanswer = ClinicalHistoryAnswer(questionnaire_id=questionnaire_id, donation_id=donation_id,
                                                      employee_id=employee_id, register_id=register_id)

        if kwargs.get('responses', None) is not None:
            clinicalhistoryanswer.responses = kwargs.get('responses')
        if kwargs.get('observations', None) is not None:
            clinicalhistoryanswer.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            clinicalhistoryanswer.register_at = kwargs.get('register_at')

        clinicalhistoryanswer.save()

        return CreateClinicalHistoryAnswer(clinicalhistoryanswer=clinicalhistoryanswer)


class UpdateClinicalHistoryAnswer(graphene.Mutation):
    clinicalhistoryanswer = graphene.Field(ClinicalHistoryAnswerType)

    class Arguments:
        id = graphene.Int(required=True)
        questionnaire_id = graphene.Int()
        donation_id = graphene.Int()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        responses = generic.GenericScalar()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['sieves.change_clinicalhistoryanswer'])
    def mutate(self, info, id, **kwargs):
        clinicalhistoryanswer = ClinicalHistoryAnswer.objects.filter(id=id).first()
        if clinicalhistoryanswer is None:
            raise ValueError('ClinicalHistoryAnswer not found')

        if kwargs.get('questionnaire_id', None) is not None:
            clinicalhistoryanswer.questionnaire_id = kwargs.get('questionnaire_id')
        if kwargs.get('donation_id', None) is not None:
            clinicalhistoryanswer.donation_id = kwargs.get('donation_id')
        if kwargs.get('employee_id', None) is not None:
            clinicalhistoryanswer.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            clinicalhistoryanswer.register_id = kwargs.get('register_id')
        if kwargs.get('responses', None) is not None:
            clinicalhistoryanswer.responses = kwargs.get('responses')
        if kwargs.get('observations', None) is not None:
            clinicalhistoryanswer.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            clinicalhistoryanswer.register_at = kwargs.get('register_at')

        clinicalhistoryanswer.save()

        return UpdateClinicalHistoryAnswer(clinicalhistoryanswer=clinicalhistoryanswer)


class Mutation(graphene.ObjectType):
    create_clinicalhistoryquestion = CreateClinicalHistoryQuestion.Field()
    update_clinicalhistoryquestion = UpdateClinicalHistoryQuestion.Field()

    create_clinicalhistoryanswer = CreateClinicalHistoryAnswer.Field()
    update_clinicalhistoryanswer = UpdateClinicalHistoryAnswer.Field()
