from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(_id=ObjectId(), email='user1@example.com', name='User One', age=25),
            User(_id=ObjectId(), email='user2@example.com', name='User Two', age=30),
            User(_id=ObjectId(), email='user3@example.com', name='User Three', age=35),
        ]
        User.objects.bulk_create(users)

        # Refresh users from the database to get their IDs
        users = list(User.objects.all())

        # Create teams
        team1 = Team(_id=ObjectId(), name='Team Alpha')
        team2 = Team(_id=ObjectId(), name='Team Beta')
        team1.save()
        team2.save()

        # Add members to teams
        team1.members.add(users[0], users[1])
        team2.members.add(users[2])

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], type='Running', duration=30, date='2025-04-01'),
            Activity(_id=ObjectId(), user=users[1], type='Cycling', duration=60, date='2025-04-02'),
            Activity(_id=ObjectId(), user=users[2], type='Swimming', duration=45, date='2025-04-03'),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), team=team1, points=100),
            Leaderboard(_id=ObjectId(), team=team2, points=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Morning Run', description='A quick morning run', duration=30),
            Workout(_id=ObjectId(), name='Evening Swim', description='Relaxing swim session', duration=45),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))