from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

class Person(models.Model):
    tmdb_id = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    biography = models.TextField()
    dayofbirth = models.DateTimeField()

class Character(models.Model):
    person = models.ForeignKey(Person)
    character = models.CharField(max_length=256)

class CrewMember(models.Model):
    person = models.ForeignKey(Person)
    job = models.CharField(max_length=256)

class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField()
    genre = models.CharField(max_length=256)

    def __unicode__(self):
        return self.genre

class Studio(models.Model):
    tmdb_id = models.PositiveIntegerField()
    studio = models.CharField(max_length=256)
    description = models.TextField()

    def __unicode__(self):
        return self.studio

class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField()
    title = models.CharField(max_length=256)
    overview = models.TextField()
    release_date = models.DateTimeField()
    imdb_id = models.CharField(max_length=256)
    popularity = models.FloatField()
    user_rating = models.FloatField()
    votes = models.PositiveIntegerField()
    adult = models.BooleanField()
    genres = models.ManyToManyField(Genre)
    studios = models.ManyToManyField(Studio)
    cast = models.ManyToManyField(Character)
    crew = models.ManyToManyField(CrewMember)

    def __unicode__(self):
        return self.title

class Poster(models.Model):
    movie = models.ForeignKey(Movie)
    w92 = models.CharField(max_length=256)
    w154 = models.CharField(max_length=256)
    w185 = models.CharField(max_length=256)
    w342 = models.CharField(max_length=256)
    w500 = models.CharField(max_length=256)
    w780 = models.CharField(max_length=256)
    original = models.CharField(max_length=256)

class Backdrop(models.Model):
    movie = models.ForeignKey(Movie)
    w300 = models.CharField(max_length=256)
    w780 = models.CharField(max_length=256)
    w1280 = models.CharField(max_length=256)
    original = models.CharField(max_length=256)

class Profile(models.Model):
    person = models.ForeignKey(Person)
    w45 = models.CharField(max_length=256)
    w185 = models.CharField(max_length=256)
    h632 = models.CharField(max_length=256)
    original = models.CharField(max_length=256)

class Logo(models.Model):
    studio = models.ForeignKey(Studio)
    w45 = models.CharField(max_length=256)
    w92 = models.CharField(max_length=256)
    w154 = models.CharField(max_length=256)
    w185 = models.CharField(max_length=256)
    w300 = models.CharField(max_length=256)
    w500 = models.CharField(max_length=256)
    original = models.CharField(max_length=256)

class Reel(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=256)
    movies = models.ManyToManyField(Movie)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")

    reels = models.ManyToManyField(Reel)

    def __unicode__(self):
        return self.user.username

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
