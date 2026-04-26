import json 
import pandas as pd
from .APIClient import *
from .utilities import json_to_class, json_default_only
from .defaultDataClass import *

NHL_API_URL = "https://api-web.nhle.com/v1"
NHL_STATS_API_URL = "https://api.nhle.com/stats/rest"


class ApiClass():
    def __init__(self):
        self.api = APIClient(NHL_API_URL) 


class ClassProp():
    def __init__(self):
        pass

    def dataToDf(self, list:list[set]):
        df = pd.DataFrame(list)
        #df.set_index("id")
        return df

    def objsToDf(self, objs):
        objs_data = []
        for obj in objs:
            objs_data.append(obj.json_data)
        return self.dataToDf(objs_data)

    @property
    def forwards_df(self):
        return self.objsToDf(self.forwards)
    
    @property
    def defensemen_df(self):
        return self.objsToDf(self.defensemen)
    
    @property
    def goalies_df(self):
        return self.objsToDf(self.goalies)
    
    @property
    def players_df(self):
        return self.objsToDf(self.players)
    
    @property
    def events_df(self):
        return self.objsToDf(self.events) 
    
    @property
    def games_df(self):
        return self.objsToDf(self.games)


class Memory_Manager(ClassProp):
    def __init__(self):
        pass

    @property
    def forwards(self):
        return Player.forward_by_id.values()
    
    @property
    def defensemen(self):
        return Player.defensemen_by_id.values()
    
    @property
    def goalies(self):
        return Player.goalies_by_id.values()

    @property
    def players(self):
        return Player.player_by_id.values()
    
    @property
    def events(self):
        return Event.event_by_id.values()
    
    @property
    def games(self):
        return Game.game_by_id.values()

    @property
    def teams(self):
        return Team.team_by_id.values()


class TeamDataBySeason(ApiClass, ClassProp):
    def __init__(self, teamId:str, seasonId):
        super().__init__()
        self.teamId = teamId
        self.seasonId = seasonId

        self.forwards :list[Player] = []
        self.defensemen :list[Player] = []
        self.goalies :list[Player] = []
        self.games :list[Game] = []


        self.load_players()
        self.load_season_games()

    def load_players(self):
        roster = self.get_roster() 

        for pl in roster["forwards"] :
            self.forwards.append(Player(pl["id"]))

        for pl in roster["defensemen"] :
            self.defensemen.append(Player(pl["id"]))

        for pl in roster["goalies"] :
            self.goalies.append(Player(pl["id"]))

    def load_season_games(self):
        sche = self.api.get("/".join(["club-schedule-season",self.teamId,str(self.seasonId)]))
        for game in sche['games']:
            self.games.append(Game(game))

    def get_season_stats(self, season:int, game_type:int=2):
        """
        Get Season Stats

        :param season: (int) - Season in YYYYYYYY format, where the first four digits \
        represent the start year of the season, and the last four digits represent the end year.
        :param game_type: (int) - Game type (guessing 2 for regular season, 3 for playoffs)
        :return: JSON response
        """
        return self.api.get("/".join(["club-stats",self.teamId,str(season),str(game_type)]))

    def get_roster(self, player_type:str="forwards"):
        """
        Get roster by season

        :param season: (int) - Season in YYYYYYYY format, where the first four digits \
        represent the start year of the season, and the last four digits represent the end year.
        :return: (list) Roaster List
        """
        return self.api.get("/".join(["roster",self.teamId,str(self.seasonId)]))
    
    
    @property
    def players(self):
        """
        Output all players
        
        :return: Players
        """
        return self.forwards+self.defensemen+self.goalies

    @property
    def events(self):
        """
        Output all events in cumulated games
        
        :return: events
        """
        events = []
        for game in self.games:
            events.extend(game.events)
        return events
    
class Team(ApiClass, ClassProp):
    """
    Team Information class from NHL API
    On specific season

    :param team: team (string) - Three-letter team code
    """
    team_by_id = {}

    def __init__(self, teamId:str):
        super().__init__()

        # Cache check
        if teamId in Team.team_by_id:
            cached = Team.team_by_id[teamId]
            # Copy cached
            self.__dict__.update(cached.__dict__)
            return
        
        self.teamId = teamId
        self.data_by_season: set[TeamDataBySeason] = {}

        Team.team_by_id[teamId] = self

    
    def load_data(self, seasonId:int):
        # Load Data by Season
        if seasonId not in self.data_by_season:
            self.data_by_season[seasonId] = TeamDataBySeason(self.teamId,seasonId)

    def get_roster_season(self):
        """
        Get a list of the seasons that the team played.
        :return: JSON response
        """
        return self.api.get("/".join(["roster-season",self.teamId]))
    

    @property
    def forwards(self):
        """
        Output all forwards from all Seasons Loaded
        
        :return: Forwards
        """
        players = []
        for season_data in self.data_by_season.values():
            players.extend(season_data.forwards)
        return players
    

    @property
    def defensemen(self):
        """
        Output all defensemen from all Seasons Loaded
        
        :return: Defensemen
        """
        players = []
        for season_data in self.data_by_season.values():
            players.extend(season_data.defensemen)
        return players
    
    @property
    def goalies(self):
        """
        Output all goalies from all Seasons Loaded
        
        :return: Goalies
        """
        players = []
        for season_data in self.data_by_season.values():
            players.extend(season_data.goalies)
        return players

    @property
    def players(self):
        """
        Output all players from all Seasons Loaded
        
        :return: Players
        """
        return self.forwards+self.defensemen+self.goalies

    @property
    def events(self):
        """
        Output all events in cumulated games
        
        :return: events
        """
        events = []
        for game in self.games:
            events.extend(game.events)
        return events
    

class Player(ApiClass, PLAYER_DEFAULTS):
    """
    Player Information class from NHL API

    :param playerId: playerId (int) - player ID
    """
    player_by_id = {}

    forward_by_id = {}
    defensemen_by_id = {}
    goalies_by_id = {}

    def __init__(self, playerId:int):
        super().__init__()

        # Cache check
        if playerId in Player.player_by_id:
            cached = Player.player_by_id[playerId]
            # Copy cached
            self.__dict__.update(cached.__dict__)
            return
        
        self.json_data = json_default_only(self.api.get("/".join(["player",str(playerId),"landing"])))
        self.json_data = {k: self.json_data.get(k) for k in self.output_json_keys}
        self = json_to_class(self, self.json_data)

        Player.player_by_id[playerId] = self


class Game(ApiClass, GAME_DEFAULTS):

    game_by_id = {}

    def __init__(self, json_data):
        super().__init__()
        self.events : list[Event] = []
        json_data = json_default_only(json_data)
        json_data = self.edit_NHL_json(json_data)
        self.json_data = {k: json_data.get(k) for k in self.output_json_keys}
        self = json_to_class(self, json_data)
        self.load_events()

        Game.game_by_id[self.id] = self

    def load_events(self):
        json_events = self.api.get("/".join(["wsc","play-by-play",str(self.id)]))
        for json_event in json_events:
            self.events.append(Event(json_default_only(json_event)))


    def edit_NHL_json(self, json_data:set):
        json_data['awayTeamId'] = json_data['awayTeam']['id']
        json_data['homeTeamId'] = json_data['homeTeam']['id']

        if 'winningGoalie' in json_data.keys():
            json_data['winningGoalieId'] = json_data['winningGoalie']['playerId']
        else: json_data['winningGoalieId'] = pd.NA

        if 'winningGoalScorer' in json_data.keys():
            json_data['winningGoalScorerId'] = json_data['winningGoalScorer']['playerId']
        else: json_data['winningGoalScorerId'] = pd.NA

        json_data['periodType'] = json_data['periodDescriptor']['periodType']

        return json_data
    

class Event(ApiClass, EVENT_DEFAULTS):

    event_by_id = {}

    def __init__(self, json_data):
        super().__init__()
        json_data = self.edit_NHL_json(json_data)
        json_data = {k: json_data.get(k) for k in self.output_json_keys}
        self = json_to_class(self, json_data)
        self.json_data = json_data

        Event.event_by_id[self.id] = self

    def edit_NHL_json(self, json_data:set):

        return json_data

