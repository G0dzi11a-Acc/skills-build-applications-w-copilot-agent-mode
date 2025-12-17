from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete existing data
        for obj in Activity.objects.all():
            if obj.id:
                obj.delete()
        for obj in Leaderboard.objects.all():
            if obj.id:
                obj.delete()
        for obj in Workout.objects.all():
            if obj.id:
                obj.delete()
        for obj in Team.objects.all():
            if obj.id:
                obj.delete()
        # Djongo workaround: delete non-superuser users in Python
        for user in User.objects.all():
            if user.id and not user.is_superuser:
                user.delete()

        # Create users (superheroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create_user(**hero, password='password') for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero, password='password') for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Marvel')
        dc_team = Team.objects.create(name='DC')
        marvel_team.members.set(marvel_users)
        dc_team.members.set(dc_users)

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(
                user=user,
                activity_type='Running',
                duration=30,
                distance=5.0,
                calories=300,
                date=timezone.now().date(),
            )
            Activity.objects.create(
                user=user,
                activity_type='Cycling',
                duration=45,
                distance=15.0,
                calories=500,
                date=timezone.now().date(),
            )

        # Create workouts
        for user in marvel_users + dc_users:
            Workout.objects.create(
                name=f"{user.username.capitalize()} Strength Workout",
                description="A superhero strength workout routine.",
                difficulty="Hard",
                duration=60,
                created_by=user
            )

        # Create leaderboard
        Leaderboard.objects.create(team=marvel_team, total_points=1000, week=1, year=2025)
        Leaderboard.objects.create(team=dc_team, total_points=900, week=1, year=2025)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
