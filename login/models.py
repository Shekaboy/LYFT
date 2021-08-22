from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Beaver(models.Model):
    phone_number_regex = RegexValidator(regex="^[1-9][0-9]{9}", message="Not a valid phone number",)
    user = models.OneToOneField(User, related_name="users", on_delete=models.CASCADE)
    phone = models.BigIntegerField(validators=[phone_number_regex])
    address = models.TextField(help_text="Click on your address", blank=False)

    class Meta:
        verbose_name_plural = "Beavers"

        def __str__(self):
            return self.address