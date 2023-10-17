from rest_framework.views import APIView, Response, status, Request
from movie.serializers import MovieSerializer, ReviewSerializer
from movie.models import Movie, Review
from rest_framework.authentication import TokenAuthentication
from movie.permissions import IsAdmin, ReviewPermission
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination 


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    
    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request):
        movies = Movie.objects.all()

        pagination = self.paginate_queryset(movies, request, self)
        serializer = MovieSerializer(pagination, many=True)

        return self.get_paginated_response(serializer.data)


class MovieByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, movie_id):
        movie = Movie.objects.get(id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer = MovieSerializer(movie, request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status.HTTP_200_OK)

        except ObjectDoesNotExist as _:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist as _:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)


class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermission]
    
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)

        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class ReviewByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermission]

    def delete(self, request, review_id):
        review = Review.objects.get(id=review_id)

        if request.user != review.user:
            return Response({"message": "This review does not belong to this review"}, status.HTTP_403_FORBIDDEN)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAllView(APIView):
    def get(self, request):
        review = Review.objects.all()

        serializer = ReviewSerializer(review, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
