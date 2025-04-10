from django.urls import path
from core.views import HelloWorldView, PingView, DbView, DatabaseInfoView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('ping/', PingView.as_view(), name='ping'),
    path('db/', DbView.as_view(), name='db'),
    path('db-info/', DatabaseInfoView.as_view(), name='db_info'),
]
