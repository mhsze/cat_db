from django.urls import reverse
from django.utils.safestring import mark_safe
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from catapp.urls.wagtail import urlpatterns as wagtail_urlpatterns


class WelcomePanel:
    order = 50

    def render(self):
        return mark_safe(
            """
        <section class="panel summary nice-padding">
          <h3>Welcome to the cat_db admin homepage!</h3>
        </section>
        """
        )


@hooks.register("construct_homepage_panels")
def add_another_welcome_panel(request, panels):
    panels.append(WelcomePanel())


@hooks.register("register_admin_urls")
def register_admin_urls():
    return wagtail_urlpatterns


class HomesMenuItem(MenuItem):
    def is_shown(self, request):
        return True


@hooks.register("register_admin_menu_item")
def register_homes_menu_item():
    return HomesMenuItem(
        "Home", reverse("cathome:index"), classnames="icon icon-snippet", order=1000
    )


class CatsMenuItem(MenuItem):
    def is_shown(self, request):
        return True


@hooks.register("register_admin_menu_item")
def register_cats_menu_item():
    return HomesMenuItem(
        "Cat", reverse("cat:index"), classnames="icon icon-snippet", order=1000
    )
