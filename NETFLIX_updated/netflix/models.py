# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CastTable(models.Model):
    cast_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cast_table'


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey('ContentTypes', models.DO_NOTHING)
    content_rating = models.ForeignKey('ContentRatings', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content'

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    class Meta:
        managed = False
        db_table = 'faq'

class Complaint(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField()
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complaint'

class TopTenMovies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image_data = models.BinaryField(blank=True, null=True)  # For binary image data
    video_data = models.BinaryField(blank=True, null=True)  # For binary video data

    class Meta:
        managed = False
        db_table = 'top_ten_movies'

class ContentCast(models.Model):
    content = models.OneToOneField(Content, models.DO_NOTHING, primary_key=True)  # The composite primary key (content_id, cast_id) found, that is not supported. The first column is selected.
    cast = models.ForeignKey(CastTable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'content_cast'
        unique_together = (('content', 'cast'),)


class ContentCrew(models.Model):
    content = models.OneToOneField(Content, models.DO_NOTHING, primary_key=True)  # The composite primary key (content_id, crew_id) found, that is not supported. The first column is selected.
    crew = models.ForeignKey('Crew', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'content_crew'
        unique_together = (('content', 'crew'),)


class ContentGenres(models.Model):
    content = models.OneToOneField(Content, models.DO_NOTHING, primary_key=True)  # The composite primary key (content_id, genre_id) found, that is not supported. The first column is selected.
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'content_genres'
        unique_together = (('content', 'genre'),)


class ContentRatings(models.Model):
    content_rating_id = models.AutoField(primary_key=True)
    rating_name = models.CharField(max_length=10)
    age_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_ratings'


class ContentTypes(models.Model):
    content_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'content_types'


class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'countries'


class Crew(models.Model):
    crew_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crew'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'genres'


class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'languages'

    def __str__(self):
        return f"{self.language_id}"


class NetflixUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'netflix_user'



class SubscriptionPlans(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_screens = models.IntegerField(blank=True, null=True)
    quality = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription_plans'


class Subscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    plan = models.ForeignKey(SubscriptionPlans, models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'subscriptions'

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone
import base64

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.SET_NULL, null=True, blank=True, default=1)  # Default to English (ID: 1)
    subscription_plan = models.CharField(max_length=50, blank=True, null=True)  # New field to store the subscription plan

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.full_name if self.full_name else self.email} (ID: {self.user_id})"


class UserProfiles(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    profile_name = models.CharField(max_length=100)
    language = models.ForeignKey(Languages, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profiles'


class WatchHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(UserProfiles, models.DO_NOTHING)
    content = models.ForeignKey(Content, models.DO_NOTHING)
    watched_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'watch_history'


class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(UserProfiles, models.DO_NOTHING)
    content = models.ForeignKey(Content, models.DO_NOTHING)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'watchlist'



class AppMovie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image_data = models.BinaryField(blank=True, null=True)  # For binary image data
    video_data = models.BinaryField(blank=True, null=True)  # For binary video data

    class Meta:
        managed = False
        db_table = 'app_movie'

class MyMovieList(models.Model):
    movie = models.ForeignKey(AppMovie, models.DO_NOTHING, blank=True, null=True)
    video_data = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_movie_list'

class HorrorMovies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image_data = models.BinaryField(blank=True, null=True)  # For binary image data
    video_data = models.BinaryField(blank=True, null=True)  # For binary video data

    class Meta:
        managed = False
        db_table = 'horror_movies'

class Season(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)  # For binary image data
    video_data = models.BinaryField(blank=True, null=True)  # For binary video data
    season_number = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'seasons'


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    release_date = models.DateField(null=True, blank=True)  # Allow null and blank values
    video_data = models.BinaryField(blank=True, null=True)  # For binary video data
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        managed = False
        db_table = 'episodes'

    def __str__(self):
        return f"{self.season} - {self.title}"




class MyMovieList1(models.Model):
    movie = models.ForeignKey(HorrorMovies, models.DO_NOTHING, blank=True, null=True)
    video_data = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_movie_list1'
