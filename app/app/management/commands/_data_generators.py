from app.models import Question, User, Profile, Tag, Answer, QuestionVote, AnswerVote

from django.db.models import Max
from django.conf import settings

from itertools import islice
import random
import os


def generate(generator, *, batch_size=64):
    while True:
        batch = list(islice(generator, batch_size))
        if not batch:
            break

        batch[0].__class__.objects.bulk_create(batch, batch_size)


def tag_generator(fake, ratio):
    for _ in range(ratio):
        yield Tag(
            name=fake.unique.word(),
            usages_count=fake.random_int(min=0, max=1000),
        )


def user_generator(fake, ratio):
    for _ in range(ratio):
        yield User(
            username=fake.unique.user_name(),
            email=fake.unique.free_email(),
            password=fake.password(),
        )


def profile_generator(fake, ratio):
    avatars = os.listdir(settings.BASE_DIR / 'uploads/avatars/')

    for user_id in range(1, ratio + 1):
        yield Profile(
            user_id=user_id,
            avatar=f'avatars/{random.choice(avatars)}',
            rating=fake.random_int(min=0, max=3000),
        )


def question_generator(fake, ratio):
    max_user_id = User.objects.all().aggregate(Max('id'))['id__max']

    for _ in range(ratio):
        yield Question(
            user_id=random.randint(1, max_user_id),
            title=fake.sentence(nb_words=random.randint(3, 10)),
            content=fake.text(max_nb_chars=random.randint(30, 100)),
            score=random.randint(-10, 100),
            answers_count=random.randint(0, 100),
        )


def answer_generator(fake, ratio):
    max_user_id = User.objects.all().aggregate(Max('id'))['id__max']
    max_question_id = Question.objects.all().aggregate(Max('id'))['id__max']

    for _ in range(ratio):
        yield Answer(
            user_id=random.randint(1, max_user_id),
            question_id=random.randint(1, max_question_id),
            content=fake.text(max_nb_chars=random.randint(30, 100)),
            is_correct=(not random.randint(0, 3)),
            score=random.randint(-10, 100),
        )


def question_votes_generator(ratio):
    max_user_id = User.objects.all().aggregate(Max('id'))['id__max']
    max_question_id = Question.objects.all().aggregate(Max('id'))['id__max']

    average_votes_per_user = ratio // max_user_id
    for user_id in range(1, max_user_id + 1):
        question_ids = set()
        while len(question_ids) < average_votes_per_user:
            question_ids.add(random.randint(1, max_question_id))

        for question_id in question_ids:
            yield QuestionVote(
                user_id=user_id,
                question_id=question_id,
                vote_type=('u', 'd')[random.randint(0, 1)],
            )


def answer_votes_generator(ratio):
    max_user_id = User.objects.all().aggregate(Max('id'))['id__max']
    max_answer_id = Answer.objects.all().aggregate(Max('id'))['id__max']

    average_votes_per_user = ratio // max_user_id
    for user_id in range(1, max_user_id + 1):
        answer_ids = set()
        while len(answer_ids) < average_votes_per_user:
            answer_ids.add(random.randint(1, max_answer_id))

        for answer_id in answer_ids:
            yield AnswerVote(
                user_id=user_id,
                answer_id=answer_id,
                vote_type=('u', 'd')[random.randint(0, 1)],
            )


def add_tags():
    max_question_id = Question.objects.all().aggregate(Max('id'))['id__max']
    max_tag_id = Tag.objects.all().aggregate(Max('id'))['id__max']

    for question_id in range(1, max_question_id + 1):
        question = Question.objects.get(pk=question_id)
        question.tags.set({random.randint(1, max_tag_id) for _ in range(random.randint(0, 5))})
        question.save()
