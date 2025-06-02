from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView as T
from django.views.generic.base import View as V


class TemplateView(LoginRequiredMixin, T):
    pass


class View(LoginRequiredMixin, V):
    pass
