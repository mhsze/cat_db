from django.conf.urls import include, url

from catapp.cms_views import cat, home

# app_name = "cathome"

home_urlpatterns = [
    url(r"^$", home.index, name="index"),
    url(r"^add/$", home.add, name="add"),
    url(r"^(?P<home_id>[0-9]+)/edit/$", home.edit, name="edit"),
    url(r"^(?P<home_id>[0-9]+)/delete/$", home.delete, name="delete"),
]
cat_urlpatterns = [
    url(r"^$", cat.index, name="index"),
    url(r"^add/$", cat.add, name="add"),
    url(r"^(?P<cat_id>[0-9]+)/edit/$", cat.edit, name="edit"),
    url(r"^(?P<cat_id>[0-9]+)/delete/$", cat.delete, name="delete"),
]

# URL patterns for Wagtail
urlpatterns = [
    url(r"^home/", include((home_urlpatterns, "cathome"))),
    url(r"^cat/", include((cat_urlpatterns, "cat"))),
]
