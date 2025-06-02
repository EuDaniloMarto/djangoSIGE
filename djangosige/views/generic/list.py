from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView as L


class ListView(LoginRequiredMixin, L):
    pass
