
from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = _("Reviews")

    def ready(self):
        if not apps.is_installed('pagination'):
            raise Exception('`mp-reviews depends on `mp-pagination``')

        if not apps.is_installed('captcha'):
            raise Exception('`mp-reviews depends on `django-recaptcha``')

        if not apps.is_installed('modal'):
            raise Exception('`mp-reviews depends on `mp-modal``')

        if not apps.is_installed('djmail'):
            raise Exception('`mp-reviews depends on `djmail``')
