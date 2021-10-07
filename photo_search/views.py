from pathlib import Path
from django.views.generic import TemplateView
from .utils import search_for_images

BASE_TEMPLATES_DIR = Path('photo_search')


class IndexView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'index.html'


class SearchView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'search.html'

    def get_images(self) -> dict:
        query = self.request.GET.get('q')
        if query is None:
            return {}
        return search_for_images(query).get('data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_result': self.get_images()
        })
        return context
