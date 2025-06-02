from .base import TemplateView, View
from .detail import DetailView
from .edit import CreateView, DeleteView, FormView, UpdateView
from .list import ListView

__all__ = [
    "View",
    "TemplateView",
    "DetailView",
    "CreateView",
    "DeleteView",
    "FormView",
    "UpdateView",
    "ListView",
]
