from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from djmail import mail_managers
from modal.views import ModalFormView
from pagination import PaginationMixin

from reviews.forms import ReviewForm
from reviews.models import Review


class ReviewListView(PaginationMixin, ListView):

    queryset = Review.objects.filter(is_active=True)
    paginate_by = 20
    template_name = 'reviews/list.html'


class CreateReviewView(ModalFormView):

    form_class = ReviewForm
    template_name = 'reviews/modal.html'

    def get_initial(self):

        user = self.request.user

        if user.is_authenticated and hasattr(user, 'profile'):
            return {**self.initial, 'mobile': user.profile.mobile}

        return self.initial

    def save_form(self, form):

        obj = form.save(commit=False)

        if self.request.user.is_authenticated:
            obj.user = self.request.user

        obj.answer = ''

        obj.save()

        context = {'object': obj, 'site': Site.objects.get_current()}

        mail_managers(
            '{} #{}'.format(_('New review'), obj.id),
            render_to_string('reviews/email.html', context)
        )

        return obj

    def get_success_context(self, obj):
        return {'message': _('Review was successfully sent')}
