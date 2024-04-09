from app.management.commands._data_generators import (
    generate,
    user_generator,
    profile_generator,
    question_generator,
    answer_generator,
    question_votes_generator,
    answer_votes_generator,
    tag_generator,
    add_tags
)

from django.core.management import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Fill db with generated data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Indicates the amount of data to be generated.', default=100)

    def handle(self, *args, **options):
        fake = Faker()
        ratio = options['ratio']

        self.stdout.write('generating users...')
        generate(user_generator(fake, ratio))

        self.stdout.write('generating profiles...')
        generate(profile_generator(fake, ratio))

        self.stdout.write('generating tags...')
        generate(tag_generator(fake, ratio))

        self.stdout.write('generating questions...')
        generate(question_generator(fake, 10 * ratio))

        self.stdout.write('generating answers...')
        generate(answer_generator(fake, 100 * ratio))

        self.stdout.write('generating question votes...')
        generate(question_votes_generator(100 * ratio))

        self.stdout.write('generating answer votes...')
        generate(answer_votes_generator(100 * ratio))

        self.stdout.write('adding tags to questions...')
        add_tags()

        self.stdout.write(self.style.SUCCESS('done!'))
