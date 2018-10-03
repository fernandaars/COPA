from django.conf.urls import url

from .functions import RestFunctions

# REST URLS
urlpatterns = [url(r"^pools$", RestFunctions.pool,
                   name="REST_pool"),
               url(r"^container$", RestFunctions.container,
                   name="REST_container"),
               url(r"^image$", RestFunctions.image,
                   name="REST_image"),
               ]
