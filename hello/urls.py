from django.urls import path
from hello import views
from hello.views import Home
from hello.auth import Signup, Login, Logout

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('school/', views.school, name='school'),
    path('profile/<slug:slug>/', views.profile_view, name='profile'),
    path('student', views.update_student, name='student'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('sendmail', views.send_message, name='send_message' ),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('update/<int:id>/', views.update, name='update'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    
]
