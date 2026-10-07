from django.core.management.base import BaseCommand
from core.models import FoodItem


class Command(BaseCommand):
    help = "Add test.jpg to all food items"

    def handle(self, *args, **kwargs):
        items = FoodItem.objects.all()

        count = 0

        for item in items:
            item.image = "food/test.jpg"
            item.save(update_fields=["image"])
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Image added to {count} food items."
            )
        )