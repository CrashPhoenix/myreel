from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

class Genre(models.Model):
    genre = models.CharField(max_length=256)

    def __unicode__(self):
        return self.genre

class Movie(models.Model):
    rt_id = models.PositiveIntegerField()
    title = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)
    mpaa_rating = models.CharField(max_length=256)
    runtime = models.PositiveIntegerField()
    critics_consensus = models.CharField(max_length=256)
    release_date = models.CharField(max_length=256)
    synopsis = models.TextField()
    studio = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Ratings(models.Model):
    movie = models.ForeignKey(Movie)
    critics_rating = models.CharField(max_length=256)
    critics_score = models.SmallIntegerField()
    audience_rating = models.CharField(max_length=256)
    audience_score = models.SmallIntegerField()

class Posters(models.Model):
    movie = models.ForeignKey(Movie)
    thumbnail = models.CharField(max_length=256)
    profile = models.CharField(max_length=256)
    detailed = models.CharField(max_length=256)
    original = models.CharField(max_length=256)

class Actor(models.Model):
    name = models.CharField(max_length=256)

class AbridgedCast(models.Model):
    movie = models.ForeignKey(Movie)
    actors = models.ManyToManyField(Actor)

class Director(models.Model):
    name = models.CharField(max_length=256)

class AbridgedDirectors(models.Model):
    movie = models.ForeignKey(Movie)
    directors = models.ManyToManyField(Director)

class Studio(models.Model):
    studio = models.CharField(max_length=256)

class Links(models.Model):
    movie = models.ForeignKey(Movie)
    self = models.CharField(max_length=256)
    cast = models.CharField(max_length=256)
    clips = models.CharField(max_length=256)
    reviews = models.CharField(max_length=256)
    similar = models.CharField(max_length=256)

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
