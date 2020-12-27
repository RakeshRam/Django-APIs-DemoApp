from django.contrib import admin
from .models import Author, Award, AwardRecord, Publisher, Book, ExtendUser

from django.apps import apps

# Register your models here.

admin.site.register(Author)
admin.site.register(Award)
admin.site.register(AwardRecord)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(ExtendUser)


# Gets All tables with 'graphql_auth' and registers in admin page.
app = apps.get_app_config('graphql_auth')
for model_name, model in app.models.items():
    admin.site.register(model)