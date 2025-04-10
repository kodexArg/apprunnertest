from django.urls import path
from core.views import HelloWorldView, PingView, DbView, DatabaseInfoView
from django.http import HttpResponse

def health_check(request):
  return HttpResponse("OK", status=200)


urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('ping/', PingView.as_view(), name='ping'),
    path('db/', DbView.as_view(), name='db'),
    path('db-info/', DatabaseInfoView.as_view(), name='db_info'),
    path('healthz/', health_check, name='health_check'),
]
