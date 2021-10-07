from django.urls import re_path
from .views import IndexView, SearchView, upload


urlpatterns = [
    re_path(r'search/?', SearchView.as_view(), name='search'),
    re_path(r'upload_file/?', upload, name='upload_file'),
    re_path(r'', IndexView.as_view(), name='index'),
]
