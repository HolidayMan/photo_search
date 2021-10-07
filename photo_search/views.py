import os
from pathlib import Path

from django.http import HttpResponse
from django.views.generic import TemplateView

from photo_search_iitsyndicate.settings import BASE_DIR
from .utils import search_for_images, build_email_text
from .celery_tasks import send_emails_from_file


BASE_TEMPLATES_DIR = Path('photo_search')


class IndexView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'index.html'


class SearchView(TemplateView):
    template_name = BASE_TEMPLATES_DIR / 'search.html'

    def get_images(self) -> dict:
        query = self.request.GET.get('q')
        if query is None:
            return {}
        data = search_for_images(query).get('data')
        self.request.session['search_result'] = data
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_result': self.get_images()
        })
        return context


def upload_file(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed", 403)
    file = request.FILES['file']
    if not os.path.exists(BASE_DIR / 'email_files'):
        os.mkdir(BASE_DIR / 'email_files')

    with open(BASE_DIR / 'email_files' / file.name, 'wb') as f:  # NOTE: it will rewrite existing file with the same name if one exists
        for chunk in file.chunks():
            f.write(chunk)

    send_emails_from_file.delay(file.name, build_email_text(request.session.get('search_result')))

    return HttpResponse("File uploaded successfully!")
