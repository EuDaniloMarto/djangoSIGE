from django.views.generic.base import ContextMixin


class PaginaMixin(ContextMixin):
    extra_context = {"pagina": "cadastros"}
