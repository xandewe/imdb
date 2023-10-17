from rest_framework import serializers
from movie.models import Movie, Genre, Review


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    premiere = serializers.DateTimeField()
    duration = serializers.CharField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres = validated_data.pop('genres')

        movie = Movie.objects.create(**validated_data)

        for genre in genres:
            gen, _ = Genre.objects.get_or_create(**genre)
            gen.movies.add(movie)
        
        return movie

    def update(self, instance, validated_data):
        if validated_data.get('genres'):
            genres = validated_data.pop('genres')
            for genre in genres:
                gen, _ = Genre.objects.get_or_create(**genre)
                gen.movies.add(instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers', 'recomendation', 'movie_id', 'user']
        read_only_fields = ['user']
        extra_kwargs = {"stars": {"min_value": 1, "max_value": 10}}

    def create(self, validated_data):
        user = validated_data.pop('user')
        movie = validated_data.pop('movie')

        review = Review(**validated_data, user=user, movie=movie)
        review.save()

        return review

