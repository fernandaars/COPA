from django.contrib import admin

from .models import Configuration, TierClass, Pool, Container, Image


# Register your models here.
admin.site.register(Configuration)
admin.site.register(TierClass)
admin.site.register(Pool)
admin.site.register(Container)
admin.site.register(Image)
