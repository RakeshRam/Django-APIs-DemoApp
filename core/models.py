from django.db import models
from django.contrib.auth.models import AbstractUser

class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Award(models.Model):
    CATEGORY_CHOICE = (('Doc', 'Documentary'),
                        ('Ent', 'Entertainment'),
                        ('Sci-Fi', 'Science-Fiction'),
                        ('Nov', 'Novel'))

    name = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE)

    def __str__(self):
        return f"{self.name}({self.country})"

class AwardRecord(models.Model):
    name = models.ForeignKey(Award, related_name='award_record', on_delete=models.CASCADE)
    awarded_on = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}({self.awarded_on})"

class Author(models.Model):
    name = models.CharField(max_length=100, blank=False)
    age = models.IntegerField(blank=True)
    award = models.ManyToManyField(AwardRecord, related_name="author_award")

    def __str__(self):
        return f"{self.name}"

class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    award = models.ManyToManyField(AwardRecord, related_name="publisher_award")

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    name = models.CharField(max_length=100, blank=False)
    author = models.ManyToManyField(Author, related_name="authors")
    publisher = models.ForeignKey(Publisher, related_name='book_publisher', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    award = models.ManyToManyField(AwardRecord, related_name="book_award")

    def __str__(self):
        return f"{self.name}({self.publisher.name})"

