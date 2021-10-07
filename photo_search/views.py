import os
from pathlib import Path

from django.http import HttpResponse
from django.views.generic import TemplateView

from photo_search_iitsyndicate.settings import BASE_DIR
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


def upload(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed", 403)
    file = request.FILES['file']
    if not os.path.exists(BASE_DIR / 'email_files'):
        os.mkdir(BASE_DIR / 'email_files')

    with open(BASE_DIR / 'email_files' / file.name, 'wb') as f:  # NOTE: it will rewrite existing file with the same name if one exists
        for chunk in file.chunks():
            f.write(chunk)

    return HttpResponse("File uploaded successfully!")
