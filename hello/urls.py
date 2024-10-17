from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path('school/', views.school, name='school'),
    path('profile/<int:id>', views.profile_view, name='profile')
]
