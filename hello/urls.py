from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path('school/', views.school, name='school'),
    path('profile/<slug:slug>/', views.profile_view, name='profile'),
    path('student', views.update_student, name='student'),
    path('delete/<int:id>/', views.delete, name='delete')
]
