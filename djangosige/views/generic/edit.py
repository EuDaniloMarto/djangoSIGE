from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView as C
from django.views.generic.edit import DeleteView as D
from django.views.generic.edit import FormView as F
from django.views.generic.edit import UpdateView as U


class CreateView(LoginRequiredMixin, C):
    pass


class DeleteView(LoginRequiredMixin, D):
    pass


class FormView(LoginRequiredMixin, F):
    pass


class UpdateView(LoginRequiredMixin, U):
    pass
