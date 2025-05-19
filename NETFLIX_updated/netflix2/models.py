# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class AppMovie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.CharField(max_length=100)
    video = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'app_movie'


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


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    image = models.ForeignKey('NetflixImage', models.DO_NOTHING)
    user = models.ForeignKey('NetflixUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment'


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


class HorrorMovies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.CharField(max_length=255)
    video = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'horror_movies'

from django.utils import timezone

class Image(models.Model):
    post_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('Users', on_delete=models.DO_NOTHING, null=True, blank=True)  # Allow null user
    image_name = models.CharField(max_length=255)
    image_data = models.BinaryField()
    description = models.TextField(null=True, blank=True)  # New description field
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)  # Set default to current date and time

    class Meta:
        managed = False
        db_table = 'image'

class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'languages'


class Like(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    image = models.ForeignKey(Image, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'like'
        unique_together = (('user', 'image'),)


class Netflix2Temp(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'netflix2_temp'


class NetflixCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'netflix_customuser'


class NetflixCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'netflix_customuser_groups'


class NetflixCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'netflix_customuser_user_permissions'


class NetflixImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255)
    image_data = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('NetflixUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'netflix_image'


class NetflixLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    image = models.ForeignKey(NetflixImage, models.DO_NOTHING)
    user = models.ForeignKey('NetflixUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'netflix_like'
        unique_together = (('user', 'image'),)


class NetflixUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'netflix_users'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    language = models.ForeignKey(Languages, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
