from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcome),
	path('index/', views.index),
	path('index/<int:catergory>/', views.index),
	path('index/<int:catergory>/<int:page>', views.index),
]
