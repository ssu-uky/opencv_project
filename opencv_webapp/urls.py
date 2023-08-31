from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

app_name = "opencv_webapp"

urlpatterns = [
    path("", views.first_view, name="first_view"),  # 127.0.0.1:8000
    path("simple_upload/", views.simple_upload, name="simple_upload"),
    path('detect_face/', views.detect_face, name='detect_face'),
]

# MEDIA_URL 은 위의 urlpattern에 추가
# document_root 는 실제로 파일이 존재하는 위치
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
