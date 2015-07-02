import urllib
import urllib2
import xml.etree.ElementTree as ET
import time
import datetime
import sys

def convert_to_timestamp(date_string):
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

def concat(values):
    return ','.join([str(s) for s in values])

class Api:

    def __init__(self, year):
        mfl_url = 'http://football.myfantasyleague.com'
        self.mfl_export_url = '{}/{}/export'.format(mfl_url, year)

    def _export(self, params, json=True):
        if json:
            params['JSON'] = 1
        encoded_params = urllib.urlencode(params)
        url = '{}?{}'.format(self.mfl_export_url, encoded_params)
        resp = urllib2.urlopen(url)
        return json.loads(resp.read())

    def players(self, players=None, since=None, details=False):
        params = {'TYPE': 'players'}
        if details:
            params['DETAILS'] = 1
        if since is not None:
            timestamp = convert_to_timestamp(since)
            params['SINCE'] = timestamp
        if players is not None:
            params['PLAYERS'] = concat(players)
        return self._export(params)

    def all_rules(self):
        params = {'TYPE': 'allRules'}
        return self._export(params)

    def injuries(self, week=None):
        params = {'TYPE': 'injuries'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def nfl_schedule(self, week=None):
        params = {'TYPE': 'nflSchedule'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def adp(self,
            franchises=None,
            is_mock=None,
            is_ppr=None,
            is_keeper=None,
            time=None,
            days=None):
        params = {'TYPE': 'adp'}
        if franchises is not None:
            params['FRANCHISES'] = franchises
        if is_mock:
            params['IS_MOCK'] = 1
        elif not is_mock and is_mock is not None:
            params['IS_MOCK'] = 0
        if is_ppr:
            params['IS_PPR'] = 1
        elif not is_ppr and is_ppr is not None:
            params['IS_PPR'] = 0
        if is_keeper:
            params['IS_KEEPER'] = 1
        elif not is_keeper and is_keeper is not None:
            params['IS_KEEPER'] = 0
        if time is not None:
            params['TIME'] = convert_to_timestamp(time)
        if days is not None:
            params['DAYS'] = days
        return self._export(params)

    """
    Actual AAV API call only supports FRANCHISES, but could eventually use the other AAV endpoint:
    http://football.myfantasyleague.com/2013/aav?COUNT=32&POS=*&CUTOFF=5&FRANCHISES=-1&IS_PPR=0&IS_KEEPER=0&TIME=
    """
    def aav(self, franchises=None):
        params = {'TYPE': 'aav'}
        if franchises is not None:
            params['FRANCHISES'] = franchises
        return self._export(params)

    def top_adds(self, week=None):
        params = {'TYPE': 'topAdds'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_drops(self, week=None):
        params = {'TYPE': 'topDrops'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_starters(self, week=None):
        params = {'TYPE': 'topStarters'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_owns(self, week=None):
        params = {'TYPE': 'topOwns'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def league(self, league_id, password=None, franchise_id=None):
        params = {'TYPE': 'league', 'L': league_id}
        if password is not None:
            params['PASSWORD'] = password
        if franchise_id is not None:
            params['FRANCHISE_ID'] = franchise_id # must be in form of '0001'
        return self._export(params)

    def my_leagues(self):
        params = {'TYPE': 'myleagues'}
        return self._export(params)

    def rules(self, league_id):
        params = {'TYPE': 'rules', 'L': league_id}
        return self._export(params)

    def rosters(self, league_id, franchise_id=None):
        params = {'TYPE': 'rosters', 'L': league_id}
        if franchise_id is not None:
            params['FRANCHISE'] = franchise_id
        return self._export(params)

    def league_standings(self, league_id):
        params = {'TYPE': 'leagueStandings', 'L': league_id}
        return self._export(params)

    def weekly_results(self, league_id, week=None):
        params = {'TYPE': 'weeklyResults', 'L': league_id}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def live_scoring(self, league_id, week=None, details=False):
        params = {'TYPE': 'liveScoring', 'L': league_id}
        if week is not None:
            params['W'] = week
        if details:
            params['DETAILS'] = 1
        return self._export(params)

    def player_scores(self,
                      league_id,
                      week=None,
                      players=None,
                      count=None,
                      position=None,
                      status=None):
        params = {'TYPE': 'playerScores', 'L': league_id}
        if week is not None:
            params['W'] = week
        if players is not None:
            params['PLAYERS'] = concat(players)
        if count is not None:
            params['COUNT'] = count
        if position is not None:
            params['POSITION'] = position
        if status is not None:
            params['STATUS'] = status
        return self._export(params)

    def draft_results(self, league_id):
        params = {'TYPE': 'draftResults', 'L': league_id}
        return self._export(params)

    def future_draft_picks(self, league_id):
        params = {'TYPE': 'futureDraftPicks', 'L': league_id}
        return self._export(params)

    def auction_results(self, league_id):
        params = {'TYPE': 'auctionResults', 'L': league_id}
        return self._export(params)

    def free_agents(self, league_id, position=None):
        params = {'TYPE': 'freeAgents', 'L': league_id}
        if position is not None:
            params['POSITION'] = position
        return self._export(params)

    def transactions(self,
                     league_id,
                     week=None,
                     transaction_type=None,
                     franchise=None,
                     days=None,
                     count=None):
        params = {'TYPE': 'transactions', 'L': league_id}
        if week is not None:
            params['W'] = week
        if transaction_type is not None:
            params['TRANS_TYPE'] = transaction_type
        if franchise is not None:
            params['FRANCHISE'] = franchise
        if days is not None:
            params['DAYS'] = days
        if count is not None:
            params['COUNT'] = count
        return self._export(params)

    def rss(self, league_id):
        params = {'TYPE': 'rss', 'L': league_id}
        return self._export(params)

    def site_news(self):
        params = {'TYPE': 'siteNews'}
        return self._export(params)

    def projected_scores(self,
                         league_id,
                         players,
                         week=None,
                         count=None,
                         position=None,
                         status=None):
        params = {
            'TYPE': 'projectedScores',
            'L': league_id,
            'PLAYERS': concat(players)
        }
        if week is not None:
            params['W'] = week
        if count is not None:
            params['COUNT'] = count
        if position is not None:
            params['POSITION'] = position
        if status is not None:
            params['STATUS'] = status
        return self._export(params)

    def league_search(self, search_query):
        params = {'TYPE': 'leagueSearch', 'SEARCH': search_query}
        return self._export(params)

    def message_board(self, league_id, count=None):
        params = {'TYPE': 'messageBoard', 'L': league_id}
        if count is not None:
            params['COUNT'] = count
        return self._export(params)

    def message_board_thread(self, league_id, thread_id):
        params = {
            'TYPE': 'messageBoardThread',
            'L': league_id,
            'THREAD': thread_id
        }
        return self._export(params)

    def player_profile(self, players):
        params = {
            'TYPE': 'playerProfile',
            'P': concat(players)
        }
        return self._export(params)

    def player_status(self, players):
        params = {
            'TYPE': 'playerStatus',
            'P': concat(players)
        }
        return self._export(params)

    def accounting(self, league_id):
        params = {'TYPE': 'accounting', 'L': league_id}
        return self._export(params)

    def calendar(self, league_id):
        params = {'TYPE': 'calendar', 'L': league_id}
        return self._export(params)

    def ics(self, league_id):
        params = {'TYPE': 'ics', 'L': league_id}
        return self._export(params, json=False)

    def points_allowed(self, league_id):
        params = {'TYPE': 'pointsAllowed', 'L': league_id}
        return self._export(params)

    def pending_trades(self, league_id):
        params = {'TYPE': 'pendingTrades', 'L': league_id}
        return self._export(params)

    def trade_bait(self, league_id):
        params = {'TYPE': 'tradeBait', 'L': league_id}
        return self._export(params)

    def my_watch_list(self, league_id):
        params = {'TYPE': 'myWatchList', 'L': league_id}
        return self._export(params)

    def my_draft_list(self, league_id):
        params = {'TYPE': 'myDraftList', 'L': league_id}
        return self._export(params)

    def who_should_i_start(self,
                           league_id=None,
                           franchise_id=None,
                           week=None,
                           players=None):
        params = {'TYPE': 'whoShouldIStart'}
        if league_id is not None:
            params['L'] = league_id
        if franchise_id is not None:
            params['F'] = franchise_id
        if week is not None:
            params['W'] = week
        if players is not None:
            params['PLAYERS'] = concat(players)
        return self._export(params)

    def polls(self, league_id):
        params = {'TYPE': 'polls', 'L': league_id}
        return self._export(params)

    def survivor_pool(self, league_id):
        params = {'TYPE': 'survivorPool', 'L': league_id}
        return self._export(params)

    def pool(self, league_id):
        params = {'TYPE': 'pool', 'L': league_id}
        return self._export(params)

    def playoff_brackets(self, league_id):
        params = {'TYPE': 'playoffBrackets', 'L': league_id}
        return self._export(params)

    def appearance(self, league_id):
        params = {'TYPE': 'appearance', 'L': league_id}
        return self._export(params)

    def assets(self, league_id):
        params = {'TYPE': 'assets', 'L': league_id}
        return self._export(params)

    def salary_adjustments(self, league_id):
        params = {'TYPE': 'salaryAdjustments', 'L': league_id}
        return self._export(params)