from django.urls import path
from users import views

urlpatterns = [
    path('users/register/', views.UserView.as_view()),
    path('users/login/', views.LoginView.as_view()),
    path('users/', views.UserView.as_view()),
    path('users/<int:user_id>/', views.UserByIdView.as_view()),
]