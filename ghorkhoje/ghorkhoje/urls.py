from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from ghorkhoje.views import get_random_quote
from ghorkhoje.settings import MEDIA_URL, MEDIA_ROOT
from user.urls import auth_urlpatterns

api_v1_urls = [path("auth/", include(auth_urlpatterns), name="auth_urls")]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_urls), name="api_v1"),
    path("quotes/", get_random_quote, name="get_random_quotes"),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
