from pathlib import Path
from django.views.generic import TemplateView


BASE_TEMPLATES_DIR = Path('photo_search')


class IndexView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'index.html'


class SearchView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'search.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


