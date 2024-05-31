from datetime import timedelta

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import timezone


alphanumeric_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z0-9 ]*$", message="Only letters, numbers, and spaces are allowed."
)
alphabetic_space_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z ]*$", message="Only alphabetic characters and spaces are allowed."
)


class Book(models.Model):
    name = models.CharField(max_length=50, validators=[alphanumeric_validator] ,null=False , blank=False)
    author = models.CharField(max_length=50, validators=[alphabetic_space_validator], null=False , blank=False)
    count = models.PositiveIntegerField(default=1 ,blank=False , null=False)
    categories = models.ManyToManyField("Category", related_name="books")
    def borrow(self, user: User):
        if self.count > 0:
            self.count -= 1
            self.save()
            Borrow.objects.create(book=self, user=user)
            return True
        return False

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50, validators=[validators.MinLengthValidator(3)]
    )


    def __str__(self) -> str:
        return self.name


class Borrow(models.Model):
    borrowed_time = models.DateTimeField(auto_now_add=True, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")

    def has_expired(self):
        now = timezone.now()
        one_week_ago = now - timedelta(weeks=1)
        if self.borrowed_time <= one_week_ago:
            return True
        else:
            return False

    def __str__(self) -> str:
        return "{} --> {} at {}".format(
            self.user.username, self.book.name, self.borrowed_time
        )
