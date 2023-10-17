from django.urls import path
from movie import views

urlpatterns = [
    path('movies/', views.MovieView.as_view()),
    path('movies/<int:movie_id>/', views.MovieByIdView.as_view()),
    path('movies/<int:movie_id>/reviews/', views.ReviewView.as_view()),
    path('reviews/<int:review_id>/', views.ReviewByIdView.as_view()),
    path('reviews/', views.ReviewListAllView.as_view()),
]