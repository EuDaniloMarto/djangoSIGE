from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView as D


class DetailView(LoginRequiredMixin, D):
    pass
