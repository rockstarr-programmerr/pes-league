import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from . import models as m
from .forms import TeamForm, SeasonForm


#############################################
# Query
#############################################


class TeamType(DjangoObjectType):
    class Meta:
        model = m.Team
        fields = '__all__'


class SeasonType(DjangoObjectType):
    class Meta:
        model = m.Season
        fields = '__all__'


class GameType(DjangoObjectType):
    class Meta:
        model = m.Game
        fields = '__all__'


class Query(graphene.ObjectType):
    teams = graphene.List(TeamType)
    team = graphene.Field(TeamType, slug=graphene.String())
    seasons = graphene.List(SeasonType)
    season = graphene.Field(SeasonType, slug=graphene.String())
    games = graphene.List(GameType)
    game = graphene.Field(GameType, pk=graphene.ID())

    def resolve_teams(self, info):
        return m.Team.objects.all()

    def resolve_team(self, info, slug):
        return m.Team.objects.get(slug=slug)

    def resolve_seasons(self, info):
        return m.Season.objects.all()

    def resolve_season(self, info, slug):
        return m.Season.objects.get(slug=slug)

    def resolve_games(self, info):
        return m.Game.objects.all()

    def resolve_game(self, info, pk):
        return m.Game.objects.get(pk=pk)


#############################################
# Mutation
#############################################


class TeamMutation(DjangoModelFormMutation):
    class Meta:
        form_class = TeamForm


class SeasonMutation(DjangoModelFormMutation):
    class Meta:
        form_class = SeasonForm


class Mutation(graphene.ObjectType):
    team = TeamMutation.Field()
    season = SeasonMutation.Field()


#############################################
# Schema
#############################################


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
