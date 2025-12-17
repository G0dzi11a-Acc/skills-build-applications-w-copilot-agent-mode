from djongo import models
from django.contrib.auth.models import AbstractUser

# User model
class User(AbstractUser):
    from djongo.models import ObjectIdField
    id = ObjectIdField(primary_key=True, editable=False)
    # Additional fields can be added here
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='octofit_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='octofit_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Team model
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('User', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Activity model
class Activity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    distance = models.FloatField(help_text='Distance in kilometers', null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

# Leaderboard model
class Leaderboard(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='leaderboards')
    total_points = models.PositiveIntegerField(default=0)
    week = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('team', 'week', 'year')

    def __str__(self):
        return f"{self.team.name} - Week {self.week}, {self.year}"

# Workout model
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
