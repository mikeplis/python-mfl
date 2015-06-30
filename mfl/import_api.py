import urllib
import urllib2
import xml.etree.ElementTree as ET
import time
import datetime
import sys

# TODO: these are duplicated from api.py
def convert_to_timestamp(date_string):
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

def concat(values):
    return ','.join([str(s) for s in values])

class ImportApi:

    def __init__(self, year):
        opener = urllib2.build_opener()
        mfl_url = 'http://football.myfantasyleague.com'
        self.opener = opener
        self.mfl_import_url = '{}/{}/import'.format(mfl_url, year)
        self.mfl_export_url = '{}/{}/export'.format(mfl_url, year)
        self.mfl_login_url = '{}/{}/login'.format(mfl_url, year)

    _logged_in = False

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

    def franchises(self):
        pass

    def draft_results_import(self):
        pass

    def auction_results_import(self):
        pass

    def salaries(self):
        pass

    def accounting_import(self, franchise_id, amount, description):
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

    def message_board_import(self, body, thread=None, subject=None):
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
            'STARTERS': concat(starters),
            'COMMENTS': comments,
            'L': self.league_id
        }
        if tiebreakers is not None:
            params['TIEBREAKERS'] = concat(tiebreakers)
        if backups is not None:
            params['BACKUPS'] = concat(backups)
        return self._import(params)

    def fcfs_waiver(self, add=None, drop=None):
        params = {'TYPE': 'fcfsWaiver', 'L': self.league_id}
        if add is not None:
            params['ADD'] = concat(add)
        if drop is not None:
            params['DROP'] = concat(drop)
        return self._import(params)

    def waiver_request(self, round_, picks):
        params = {
            'TYPE': 'waiverRequest',
            'ROUND': round_,
            'PICKS': concat(picks),
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

    def my_watch_list_import(self, add=None, remote=None):
        params = {'TYPE': 'myWatchList', 'L': self.league_id}
        if add is not None:
            params['ADD'] = concat(add)
        if drop is not None:
            params['DROP'] = concat(drop)
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