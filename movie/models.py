from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10)
    premiere = models.DateTimeField()
    classification = models.IntegerField()
    synopsis = models.TextField()

class Genre(models.Model):
    name = models.CharField(max_length=127)

    movies = models.ManyToManyField(Movie, related_name='genres')

class Review(models.Model):
    class RecomendationChoices(models.TextChoices):
        MUST_WATCH = ('Must Watch',)
        SHOULD_WATCH = ('Should Watch',)
        AOID_WATCH = ('Avoid Watch',)
        NO_OPINION = ('No Opinion',)

    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=30,
        choices=RecomendationChoices.choices,
        default=RecomendationChoices.NO_OPINION
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reviews')
