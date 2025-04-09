from django.urls import path
from core.views import HelloWorldView, DatabaseInfoView, PingView, DbView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('database/', DatabaseInfoView.as_view(), name='database_info'),
    path('ping/', PingView.as_view(), name='ping'),
    path('db/', DbView.as_view(), name='db'),
]
