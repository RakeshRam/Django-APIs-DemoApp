from django.contrib import admin
from .models import Author, Award, AwardRecord, Publisher, Book

# Register your models here.

admin.site.register(Author)
admin.site.register(Award)
admin.site.register(AwardRecord)
admin.site.register(Publisher)
admin.site.register(Book)
