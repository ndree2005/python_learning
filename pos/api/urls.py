from django.urls import path
from api import views

#http://127.0.0.1:8000/super-admin/

app_name = 'api'
urlpatterns = [
    #path('api/v1/login', LoginView.as_view()),
    #path('api/v1/logout', LogoutView.as_view()),
    #path('api/v1/register', RegisterWaitressAPI.as_view()),
    path('api/table_resto', views.TableRestoListApiView.as_view(), name='table-resto-list'),
    path('api/table_resto/<int:id>', views.TableRestoListApiView.as_view()),
]
