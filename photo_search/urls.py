from django.urls import re_path
from .views import IndexView, SearchView


urlpatterns = [
    re_path(r'search/?', SearchView.as_view(), name='search'),
    re_path(r'', IndexView.as_view(), name='index'),
]
