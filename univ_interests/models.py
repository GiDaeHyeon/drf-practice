from django.db import models


class User(models.Model):

    class Meta:
        db_table = 'user'

    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=200)
    nickname = models.CharField(unique=True, max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Country(models.Model):

    class Meta:
        db_table = 'country'
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'name'],
                name='UQ_univ_interests_country_code_name'
            )
        ]

    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class University(models.Model):

    class Meta:
        db_table = 'university'

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    webpage = models.URLField(null=True, max_length=255)
    name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class UniversityPreference(models.Model):

    class Meta:
        db_table = 'university_preference'
        constraints = [
            models.UniqueConstraint(
                fields=['university', 'user'],
                name='UQ_univ_interests_university_preference_university_user'
            )
        ]

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
