from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin


class PaginaMixin(ContextMixin):
    extra_context = {"pagina": "cadastros"}


class FilteredPaginationMixin(MultipleObjectMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.copy()

        if "page" in query:
            query.pop("page")

        base_url = f"?{query.urlencode()}&page=" if query else "?page="

        context["base_url"] = base_url
        return context
