from django.core.management.base import BaseCommand

from ...models import Season, Team


class Command(BaseCommand):
    help = 'Add teams to existing seasons'

    def handle(self, *args, **options):
        seasons = Season.objects.all()
        teams = Team.objects.all()

        for season in seasons:
            if season.teams.count() == 0:
                season.teams.add(*teams)

        self.stdout.write(self.style.SUCCESS('Babushka is soup ready?'))
