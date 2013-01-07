from django.core.management.base import BaseCommand, CommandError
from techism.twitter import twitter


class ShortTermTwitter(BaseCommand):

    def handle(self, *args, **options):
        twitter.tweet_upcoming_events()
