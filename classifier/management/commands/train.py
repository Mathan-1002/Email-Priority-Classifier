from django.core.management.base import BaseCommand
from classifier import ml
from classifier.models import Email


class Command(BaseCommand):
    help = "Train the priority model (seed data + corrected emails)."

    def handle(self, *args, **opts):
        extra = [(ml._text(e.subject, e.body), e.priority) for e in Email.objects.filter(corrected=True)]
        ml.train(extra)
        self.stdout.write(self.style.SUCCESS(f"Trained on seed + {len(extra)} corrected emails."))

