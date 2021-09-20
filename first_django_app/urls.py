from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('adddataview', views.AddDataView.as_view(), name='adddataview')
]
