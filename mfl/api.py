import urllib
import urllib2
import xml.etree.ElementTree as ET
import time
import datetime
import sys

def convert_to_timestamp(date_string):
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

# TODO: use this
def concat(values):
    return ','.join([str(s) for s in values])

# TODO: figure out when it's okay to use [] as default instead of None
class Api:

    _logged_in = False

    def __init__(self, year):
        opener = urllib2.build_opener()
        mfl_url = 'http://football.myfantasyleague.com'
        self.opener = opener
        self.mfl_import_url = '{}/{}/import'.format(mfl_url, year)
        self.mfl_export_url = '{}/{}/export'.format(mfl_url, year)
        self.mfl_login_url = '{}/{}/login'.format(mfl_url, year)

    def _export(self, params, json=True):
        if json:
            params['JSON'] = 1
        encoded_params = urllib.urlencode(params)
        url = '{}?{}'.format(self.mfl_export_url, encoded_params)
        resp = self.opener.open(url)
        return resp.read()

    def _import(self, params, json=True):
        if json:
            params['JSON'] = 1
        encoded_params = urllib.urlencode(params)
        url = '{}?{}'.format(self.mfl_import_url, encoded_params)
        resp = self.opener.open(url)
        return resp.read()

    # To login as commissioner, franchise_id = '0000'
    def login(self, league_id, franchise_id, password):
        params = urllib.urlencode({
            'L': league_id,
            'FRANCHISE_ID': franchise_id,
            'PASSWORD': password,
            'XML': 1}) # is 'XML' required?
        url = '{}?{}'.format(self.mfl_login_url, params)
        resp = urllib2.urlopen(url)
        user_id = ET.fromstring(resp.read()).attrib['session_id']
        self.opener.addheaders.append(('Cookie', 'USER_ID={}'.format(user_id)))
        self.league_id = league_id
        self.franchise_id = franchise_id
        self._logged_in = True # may not be needed

    # export endpoints 

    def players(self, players=None, since=None, details=False):
        params = {'TYPE': 'players'}
        if details:
            params['DETAILS'] = 1
        if since is not None:
            timestamp = convert_to_timestamp(since)
            params['SINCE'] = timestamp
        if players is not None:
            params['PLAYERS'] = ','.join([str(pid) for pid in players])
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

    def standings(self, league_id):
        params = {'TYPE': 'standings', 'L': league_id}
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
            params['PLAYERS'] = ','.join([str(pid) for pid in players])
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

    # TODO: allow caller to pass in raw projected stats
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
            'PLAYERS': ','.join([str(pid) for pid in players])
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
            'P': ','.join([str(pid) for pid in players])
        }
        return self._export(params)

    def player_status(self, players):
        params = {
            'TYPE': 'playerStatus',
            'P': ','.join([str(pid) for pid in players])
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
            params['PLAYERS'] = ','.join([str(pid) for pid in players])
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

    # import endpoints

    def franchises(self):
        pass

    def draft_results(self):
        pass

    def auction_results(self):
        pass

    def salaries(self):
        pass

    def accounting(self, franchise_id, amount, description):
        params = {
            'TYPE': 'accounting',
            'FRANCHISE_ID': franchise_id,
            'AMOUNT': amount,
            'DESCRIPTION': description,
            'L': self.league_id
        }
        return self._import(params)

    def franchise_score_adjustment(self, franchise_id, week, points, explanation):
        params = {
            'TYPE': 'franchiseScoreAdjustment',
            'FRANCHISE_ID': franchise_id,
            'WEEK': week,
            'POINTS': points,
            'EXPLANATION': explanation,
            'L': self.league_id
        }
        return self._import(params)

    def player_score_adjustment(self, player_id, week, points, explanation):
        params = {
            'TYPE': 'playerScoreAdjustment',
            'PLAYER': player_id,
            'WEEK': week,
            'POINTS': points,
            'EXPLANATION': explanation,
            'L': self.league_id
        }
        return self._import(params)

    def message_board(self, body, thread=None, subject=None):
        params = {
            'TYPE': 'messageBoard',
            'BODY': body,
            'L': self.league_id
        }
        if thread is not None:
            params['THREAD'] = thread
        if subject is not None:
            params['SUBJECT'] = subject
        return self._import(params)

    def lineup(self, week, starters, comments='', tiebreakers=None, backups=None):
        params = {
            'TYPE': 'lineup',
            'W': week,
            'STARTERS': ','.join([str(pid) for pid in starters]),
            'COMMENTS': comments,
            'L': self.league_id
        }
        if tiebreakers is not None:
            params['TIEBREAKERS'] = ','.join([str(pid) for pid in tiebreakers])
        if backups is not None:
            params['BACKUPS'] = ','.join([str(pid) for pid in backups])
        return self._import(params)

    def fcfs_waiver(self, add=None, drop=None):
        params = {'TYPE': 'fcfsWaiver', 'L': self.league_id}
        if add is not None:
            params['ADD'] = ','.join([str(pid) for pid in add])
        if drop is not None:
            params['DROP'] = ','.join([str(pid) for pid in drop])
        return self._import(params)

    def waiver_request(self, round_, picks):
        params = {
            'TYPE': 'waiverRequest',
            'ROUND': round_,
            'PICKS': ','.join([str(pid) for pid in picks]),
            'L': self.league_id
        }
        return self._import(params)

    def ir(self, activate=None, deactivate=None):
        params = {'TYPE': 'IR', 'L': self.league_id}
        if activate is not None:
            params['ACTIVATE'] = concat(activate)
        if deactivate is not None:
            params['DEACTIVATE'] = concat(deactivate)
        return self._import(params)

    def taxi_squad(self, promote=None, demote=None):
        params = {'TYPE': 'taxiSquad', 'L': self.league_id}
        if promote is not None:
            params['PROMOTE'] = concat(promote)
        if demote is not None:
            params['DEMOTE'] = concat(demote)
        return self._import(params)

    def my_watch_list(self, add=None, remote=None):
        params = {'TYPE': 'myWatchList', 'L': self.league_id}
        if add is not None:
            params['ADD'] = ','.join([str(pid) for pid in add])
        if drop is not None:
            params['DROP'] = ','.join([str(pid) for pid in drop])
        return self._import(params)

    def poll_vote(self, poll_id, answer_id):
        params = {
            'TYPE': 'pollVote',
            'POLL_ID': poll_id,
            'ANSWER_ID': answer_id,
            'L': self.league_id
        }
        return self._import(params)

    def trade_proposal(self,
                       offered_to,
                       will_give_up,
                       will_receive,
                       comments='',
                       expires=None):
        params = {
            'TYPE': 'tradeProposal',
            'OFFERED_TO': offered_to,
            'WILL_GIVE_UP': concat(will_give_up),
            'WILL_RECEIVE': concat(will_receive),
            'COMMENTS': comments,
            'L': self.league_id
        }
        if expires is not None:
            params['EXPIRES'] = convert_to_timestamp(expires)
        return self._import(params)

    def trade_response(self,
                       offered_to,
                       will_give_up,
                       offering_team,
                       response):
        params = {
            'TYPE': 'tradeResponse',
            'OFFERED_TO': offered_to,
            'WILL_GIVE_UP': will_give_up,
            'OFFERINGTEAM': offering_team,
            'RESPONSE': response,
            'L': self.league_id
        }
        return self._import(params)

    def survivor_pool_pick(self, pick):
        params = {
            'TYPE': 'survivorPoolPick',
            'PICK': pick,
            'L': self.league_id
        }
        return self._import(params)

    def pool_picks(self):
        pass

    def calendar_event(self):
        pass

    def email_message(self):
        pass
