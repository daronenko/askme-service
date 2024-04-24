from app.models import Question, Answer, Profile, User, Tag, QuestionVote, AnswerVote

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Remove data from database'

    def handle(self, *args, **options):
        models = [Question, Answer, Profile, User, Tag, QuestionVote, AnswerVote]
        for model in models:
            model.objects.all().delete()
