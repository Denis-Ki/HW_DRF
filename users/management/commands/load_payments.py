from django.core.management.base import BaseCommand
from users.models import User, Payment
from cours.models import Course


class Command(BaseCommand):
    help = "Loads payment data into the database"

    def handle(self, *args, **options):
        payment_data = [
            {
                "user": User.objects.get(pk=1),
                "payment_date": "2023-02-01T01:00:00Z",
                "paid_course": Course.objects.get(pk=1),
                "amount": "300.00",
                "payment_method": "cash",
            },
            {
                "user": User.objects.get(pk=1),
                "payment_date": "2024-02-01T01:00:00Z",
                "paid_course": Course.objects.get(pk=1),
                "amount": "200.00",
                "payment_method": "cash",
            }
        ]

        for data in payment_data:
            payment = Payment(**data)
            payment.save()

        self.stdout.write(self.style.SUCCESS("Payment data loaded successfully!"))
