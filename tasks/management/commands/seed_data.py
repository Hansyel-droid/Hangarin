from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from tasks.models import Priority, Category, Task, Note, SubTask

fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding priorities...')
        priority_names = ['High', 'Medium', 'Low', 'Critical', 'Optional']
        priorities = []
        for name in priority_names:
            p, _ = Priority.objects.get_or_create(name=name)
            priorities.append(p)

        self.stdout.write('Seeding categories...')
        category_names = ['Work', 'School', 'Personal', 'Finance', 'Projects']
        categories = []
        for name in category_names:
            c, _ = Category.objects.get_or_create(name=name)
            categories.append(c)

        self.stdout.write('Seeding tasks...')
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )

            for _ in range(random.randint(1, 3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

            for _ in range(random.randint(1, 4)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
