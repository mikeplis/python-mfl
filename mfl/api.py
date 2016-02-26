import urllib
import urllib2
import xml.etree.ElementTree as ET
import json
import time
import datetime
import sys

"""A library that provides a Python interface to the MyFantasyLeague (MFL) API."""

def convert_to_timestamp(date_string):
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

def concat(values):
    return ','.join([str(s) for s in values])

class Api:
    """A python interface to the MFL export API."""

    def __init__(self, year):
        """Create an instance of the MFL API.

        Args:
            year (int): The year to get data for (e.g. 2013).

        """
        mfl_url = 'http://football.myfantasyleague.com'
        self.mfl_export_url = '{}/{}/export'.format(mfl_url, year)

    def _export(self, params):
        """Send request to MFL API and return result.

        Used by all other methods inside the API class to create a correctly formatted request string.

        Args:
            params (dict): Parameters to be added to the request's query string.

        Returns:
            dict: Dictionary containing JSON data
        """
        params['JSON'] = 1
        encoded_params = urllib.urlencode(params)
        url = '{}?{}'.format(self.mfl_export_url, encoded_params)
        resp = urllib2.urlopen(url)
        return json.loads(resp.read())

    def players(self, players=None, since=None, details=False):
        """Return player ID's and players in the MFL database.

        All other functions use player ID's, so call this function if information like names, teams, or positions are needed.

        Args:
            players (List[int]): Player ID's to return data for.
            since (str): Date from which the function should return updates. Should be formatted as mm/dd/yyyy.
            details (bool): If True, returns extra information including weight, birthdate, draft year, and ID on other
                sites like Rotoworld, ESPN, and CBS.
        """
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
        """Return all scoring rules supported by MFL.

        Contains information about whether a scoring rule is scored for players, coaches, and/or teams. Also contains the
        abbreviation for each rule that is returned as part of the `rules` function.
        """
        params = {'TYPE': 'allRules'}
        return self._export(params)

    def injuries(self, week=None):
        """Return injury information contained in official NFL injury reports.

        Returns player ID, status (Out, Probable, Suspended etc.), and details. Also contains timestamp showing when
        this information was most recently updated.

        Args:
            week (int): NFL week to get injury data for. If no value is provided, the most recent week is used.
        """
        params = {'TYPE': 'injuries'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def nfl_schedule(self, week=None):
        """Return NFL schedule information

        Returns information about each game for a particular week including kickoff time, teams involved, team rankings
        spread, and time remaining.

        Args:
            week (int): NFL week to get schedule information for. If no value is provided, the most recent week is used.
        """
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
        """Return average draft position (ADP) information

        Args:
            franchises (int): Number of franchises in leagues for which ADP data is desired. For example, if ADP data for
                10-team leagues is wanted, pass in the number 10.
            is_mock (bool): If True, only returns data for mock drafts.
            is_ppr (bool): If True, only returns data for PPR drafts.
            is_keeper (bool): If True, only returns data for keeper drafts.
            time (str): Only returns data from drafts conducted after the given date. Should be formatted as mm/dd/yyyy.
            days (int): Only returns data from drafts conducted within the last n days, where n in the integer provided.
        """
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
        """Return average auction value (AAV) information,

        Args:
            franchises (int): Number of franchises in leagues for which AAV data is desired. For example, if AAV data for
                10-team leagues is wanted, pass in the number 10.

        """
        params = {'TYPE': 'aav'}
        if franchises is not None:
            params['FRANCHISES'] = franchises
        return self._export(params)

    def top_adds(self, week=None):
        """Return information about the most-added players across all MFL leagues.

        Only players that have been added in more than 2%% of leagues will be returned.

        Args:
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.

        """
        params = {'TYPE': 'topAdds'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_drops(self, week=None):
        """Return information about the most-dropped players across all MFL leagues.

        Only players that have been dropped in more than 2%% of leagues will be returned.

        Args:
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.

        """
        params = {'TYPE': 'topDrops'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_starters(self, week=None):
        """Return information about the most-started players across all MFL leagues.

        Only players that have been started in more than 1%% of leagues will be returned.

        Args:
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.

        """
        params = {'TYPE': 'topStarters'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def top_owns(self, week=None):
        """Return information about the most-owned players across all MFL leagues.

        Only players that are owned in more than 1%% of leagues will be returned.

        Args:
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.

        """
        params = {'TYPE': 'topOwns'}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def league(self, league_id, franchise_id=None, password=None):
        """Return basic league parameters.

        Returns information like league name, roster sizes, and starting lineup requirements. If a valid password
        and franchise_id combination are supplied, it also returns otherwise private information about the owners
        like names and email addresses

        Args:
            league_id (int): 5-digit league ID
            franchise_id (str): 4-digit franchise ID
            password (str): Login password for given franchise ID
        """
        params = {'TYPE': 'league', 'L': league_id}
        if password is not None:
            params['PASSWORD'] = password
        if franchise_id is not None:
            params['FRANCHISE_ID'] = franchise_id # must be in form of '0001'
        return self._export(params)

    def rules(self, league_id):
        """Return league scoring rules.

        Rule abbreviation definitions can be found by calling `all_rules`

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'rules', 'L': league_id}
        return self._export(params)

    def rosters(self, league_id, franchise_id=None):
        """Return current rosters.

        Response includes players status (active, IR, taxi) and salary/contract information for that player if
        the given league supports those functions.

        Args:
            league_id (int): 5-digit league ID
            franchise_id (str): 4-digit franchise ID. If provided, returns roster information for just this franchise
        """
        params = {'TYPE': 'rosters', 'L': league_id}
        if franchise_id is not None:
            params['FRANCHISE'] = franchise_id
        return self._export(params)

    def league_standings(self, league_id):
        """Return current league standings.

        Args:
            league_id (int): 5-digit league ID

        Response descriptions:
            h2hw: Overall Wins
            h2hl: Overall Losses
            h2ht: Overall Ties
            divw: Divisional Wins
            divl: Divisional Losses
            divt: Divisional Ties
            divpf: Divisional Points For (Total Year-to-Date Points Scored In Divisional Games)
            confw: Conference Wins
            confl: Conference Losses
            conft: Conference Ties
            confpf: Conference Points For (Total Year-to-Date Points Scored In Conference Games)
            pf: Points For (Total Year-to-Date Point Scored)
            pa: Points Against (Total Year-to-Date Opponent Points Scored)
            avgpa: Average Points Against (Weekly Average Opponent Points Scored)
            maxpa: Maximum Points Against (Highest Weekly Points Against)
            minpa: Minimum Points Against (Lowest Weekly Points Against)
            pp: Potential Points
            bbidspent: Total Amount Spent YTD On Blind Bidding
            op: Offensive Points
            dp: Defensive Points
            pwr: Power Rank
            altpwr: Alternative Power Rank
            acct: Accounting Balance
            salary: Total Salary
            vp: Victory Points
            power_rank: The power rank for a franchise
            all_play_w: The number of all-play wins for a franchise, assuming a franchise played all other franchises each week of the season
            all_play_l: The number of all-play losses for a franchise, assuming a franchise played all other franchises each week of the season
            all_play_t: The number of all-play ties for a franchise, assuming a franchise played all other franchises each week of the season
        """
        params = {'TYPE': 'leagueStandings', 'L': league_id}
        return self._export(params)

    def weekly_results(self, league_id, week=None):
        """Return weekly results for a given league/week

        Includes scores for all starter and non-starter players for all franchises.

        Args:
            league_id (int): 5-digit league ID
            week (int/str): NFL week to get information for. If no value is provided, the most recent week is used. Also supports "YTD" for
                year-to-data data
        """
        params = {'TYPE': 'weeklyResults', 'L': league_id}
        if week is not None:
            params['W'] = week
        return self._export(params)

    def live_scoring(self, league_id, week=None, details=False):
        """Return live scoring for given league and week

        Includes each franchise's current score, how many game seconds remaining that franchise has, players who have yet to play, and
        players who are currently playing.

        Args:
            league_id (int): 5-digit league ID
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.
            details (bool): If True, also returns live scoring for non-starters
        """
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
        """Return all player scores for given league and week.

        Includes all rostered players and free agents.

        Args:
            league_id (int): 5-digit league ID
            week (int/str): NFL week to get information for. If no value is provided, the most recent week is used. Also supports "YTD" for
                year-to-date data or "AVG" for weekly average scores.
            players (List[int]): Player ID's to return data for
            count (int): Number of results to return
            position (str): Position to return results for
            status (str): Supports 'freeagent' to only return scores for free agents
        """
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
        """Return draft results for a given league.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'draftResults', 'L': league_id}
        return self._export(params)

    def future_draft_picks(self, league_id):
        """Return future draft picks for a given league.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'futureDraftPicks', 'L': league_id}
        return self._export(params)

    def auction_results(self, league_id):
        """Return auction draft results for a given league.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'auctionResults', 'L': league_id}
        return self._export(params)

    def free_agents(self, league_id, position=None):
        """Return free agents for a given league.

        Args:
            league_id (int): 5-digit league ID
            position (str): Position to return results for
        """
        params = {'TYPE': 'freeAgents', 'L': league_id}
        if position is not None:
            params['POSITION'] = position
        return self._export(params)

    def transactions(self,
                     league_id,
                     transaction_type=None,
                     franchise_id=None,
                     days=None,
                     count=None):
        """Return all transactions for a given league.

        Args:
            league_id (int): 5-digit league ID
            transaction_type (str): Kinds of transactions to return. Supported values are
                "waiver", "bbid_waiver", "trade", "ir", "taxi", "bbid_waiver_request", "survivor_pick", and "pool_pick"
            franchise_id (str): 4-digit franchise ID to return transactions for
            days (int): Limit results to transactions done within a certain number of days
            count (int): Limit results to a certain number of transactions
        """
        params = {'TYPE': 'transactions', 'L': league_id}
        if transaction_type is not None:
            params['TRANS_TYPE'] = transaction_type.upper()
        if franchise_id is not None:
            params['FRANCHISE'] = franchise
        if days is not None:
            params['DAYS'] = days
        if count is not None:
            params['COUNT'] = count
        return self._export(params)

    def rss(self, league_id):
        """Return RSS feed of important league data.

        Includes League standings, current week's live scoring, last week's fantasy results, and the five newest message board topics

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'rss', 'L': league_id}
        return self._export(params)

    def site_news(self):
        """Return RSS feed of MyFantasyLeague site news."""
        params = {'TYPE': 'siteNews'}
        return self._export(params)

    def projected_scores(self,
                         league_id,
                         players,
                         week=None,
                         count=None,
                         position=None,
                         status=None):
        """Return expected fantasy points for certains players in a given league's scoring system.

        Projections are based on fantasysharks.com.

        Args:
            league_id (int): 5-digit league ID
            players (List[int]): ID's of players to return projected scores for
            week (int): NFL week to get information for. If no value is provided, the most recent week is used.
            count (int): Number of results to return
            position (str): Position to return results for
            status (str): Supports 'freeagent' to only return scores for free agents
        """
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
        """Return MFL leagues that match a given search query.

        Case-insensitive search query must contain at least three characters. Note that the search string can either be
        the league name, the league commissioner's email address, or an owner's email address.

        Args:
            search_query (str): Query string to search leagues with
        """
        params = {'TYPE': 'leagueSearch', 'SEARCH': search_query}
        return self._export(params)

    def message_board(self, league_id, count=10):
        """Return summary of message board posts for a given league.

        Args:
            league_id (int): 5-digit league ID
            count (int): Number of message board threads to return. Default is 10.
        """
        params = {'TYPE': 'messageBoard', 'L': league_id, 'COUNT': count}
        return self._export(params)

    def message_board_thread(self, league_id, thread_id):
        """Display posts in a particular message board thread.

        Args:
            league_id (int): 5-digit league ID
            thread_id (int): ID of message board thread to return information for
        """
        params = {
            'TYPE': 'messageBoardThread',
            'L': league_id,
            'THREAD': thread_id
        }
        return self._export(params)

    def player_profile(self, players):
        """Return summary information about given players

        Includes date-of-birth, age, ADP ranking, height, and weight.

        Args:
            players (List[int]): List of players ID's to return information about
        """
        params = {
            'TYPE': 'playerProfile',
            'P': concat(players)
        }
        return self._export(params)

    def player_status(self, league_id, players):
        """Return player status in a given league.

        Returns whether a player is locked, a free agent, or on a roster.

        Args:
            league_id (int): 5-digit league ID
            players (List[int]): List of players ID's to return status of
        """
        params = {
            'TYPE': 'playerStatus',
            'L': league_id,
            'P': concat(players)
        }
        return self._export(params)

    def accounting(self, league_id):
        """Return a summary of the league accounting records.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'accounting', 'L': league_id}
        return self._export(params)

    def calendar(self, league_id):
        """Return a summary of the league calendar

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'calendar', 'L': league_id}
        return self._export(params)

    def points_allowed(self, league_id):
        """Return fantasy points allowed by each NFL team, broken down by position

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'pointsAllowed', 'L': league_id}
        return self._export(params)

    def trade_bait(self, league_id):
        """Return trade bait for all franchises.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'tradeBait', 'L': league_id}
        return self._export(params)

    def who_should_i_start(self,
                           league_id=None,
                           franchise_id=None,
                           week=None,
                           players=None):
        """Return site-wide "Who Do I Start?" data, comparing pairs of players at the same position.

        Shows what percentage of all MFL users would choose one player over another.

        Args:
            league_id (int): 5-digit league ID
            franchise_id (str): Restrict comparisons to only players on given franchise's roster
            week (int): Show comparison data for a given NFL week
            players (List[int]): Players to show comparison data for
        """
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
        """Return all current league polls.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'polls', 'L': league_id}
        return self._export(params)

    def survivor_pool(self, league_id):
        """Return all survivor pool picks.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'survivorPool', 'L': league_id}
        return self._export(params)

    def pool(self, league_id):
        """Return all NFL or fantasy pool picks.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'pool', 'L': league_id}
        return self._export(params)

    def playoff_brackets(self, league_id):
        """Return all playoff brackets.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'playoffBrackets', 'L': league_id}
        return self._export(params)

    def appearance(self, league_id):
        """Return skin, home page tabs, and modules within each tab set up by the commissioner.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'appearance', 'L': league_id}
        return self._export(params)

    def tradeable_assets(self, league_id):
        """Return all tradeable assets for all franchises.

        Include players, current year draft picks, and future draft picks

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'assets', 'L': league_id}
        return self._export(params)

    def salary_adjustments(self, league_id):
        """Return all salary adjustments for a given league.

        Args:
            league_id (int): 5-digit league ID
        """
        params = {'TYPE': 'salaryAdjustments', 'L': league_id}
        return self._export(params)