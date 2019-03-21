from django.db import models
from UserManage.models import User

#user_film_rank
class UserFilmRank(models.Model):
    name = models.CharField(max_length=10240)
    text = models.FloatField(max_length=10240)
    mod_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.name


class Film(models.Model):
    movieid = models.IntegerField()
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    imdbId = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title, self.genres