import unittest
from api import Api
import requests

class TestApi(Api):
  """Test implementation of MFL API that returns requests.Response from all methods instead of dict

  Returning requests.Response from all methods allows for testing of things like the request's status code
  """
  def _export(self, params):
    params['JSON'] = 1
    return requests.get(self.mfl_export_url, params=params)

class TestMflApiMethods(unittest.TestCase):
  def setUp(self):
    self.api = TestApi(2015)
    self.league_id = 35465
    self.players = [7260, 6997]

  def test_aav(self):
    resp = self.api.aav()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('aav' in json)
    self.assertTrue('player' in json['aav'])
    self.assertTrue(json['aav']['player'])

  def test_accounting(self):
    resp = self.api.accounting(self.league_id)
    self.assertTrue(resp.ok)

  def test_adp(self):
    resp = self.api.adp()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('adp' in json)
    self.assertTrue('player' in json['adp'])
    self.assertTrue(json['adp']['player'])

  def test_all_rules(self):
    resp = self.api.all_rules()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('allRules' in json)
    self.assertTrue('rule' in json['allRules'])
    self.assertTrue(json['allRules']['rule'])

  def test_appearance(self):
    resp = self.api.appearance(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('appearance' in json)
    self.assertTrue('tab' in json['appearance'] and 'skin' in json['appearance'])
    self.assertTrue(json['appearance']['tab'])

  def test_assets(self):
    resp = self.api.assets(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('assets' in json)
    self.assertTrue('franchise' in json['assets'])
    self.assertTrue(json['assets']['franchise'])

  def test_auction_results(self):
    resp = self.api.auction_results(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('auctionResults' in json)
    self.assertTrue('auctionUnit' in json['auctionResults'])

  def test_calendar(self):
    resp = self.api.calendar(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('calendar' in json)
    self.assertTrue('event' in json['calendar'])
    self.assertTrue(json['calendar']['event'])

  def test_draft_results(self):
    resp = self.api.draft_results(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('draftResults' in json)
    self.assertTrue('draftUnit' in json['draftResults'])

  def test_free_agents(self):
    resp = self.api.free_agents(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('freeAgents' in json)
    self.assertTrue('leagueUnit' in json['freeAgents'])

  def test_future_draft_picks(self):
    resp = self.api.future_draft_picks(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('futureDraftPicks' in json)

  def test_injuries(self):
    resp = self.api.injuries()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('injuries' in json)
    self.assertTrue('injury' in json['injuries'])

  def test_league(self):
    resp = self.api.league(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('league' in json)
    self.assertTrue(json['league'])

  def test_league_search(self):
    resp = self.api.league_search('nfl')
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('leagues' in json)
    self.assertTrue('league' in json['leagues'])
    self.assertTrue(json['leagues']['league'])

  def test_league_standings(self):
    resp = self.api.league_standings(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('leagueStandings' in json)
    self.assertTrue('franchise' in json['leagueStandings'])

  def test_live_scoring(self):
    resp = self.api.live_scoring(self.league_id, week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('liveScoring' in json)
    self.assertTrue('matchup' in json['liveScoring'])
    self.assertTrue(json['liveScoring']['matchup'])

  def test_message_board(self):
    resp = self.api.message_board(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('messageBoard' in json)
    self.assertTrue('thread' in json['messageBoard'])
    self.assertTrue(json['messageBoard']['thread'])

  def test_message_board_thread(self):
    resp = self.api.message_board_thread(self.league_id, 3571222)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('messageBoardThread' in json)

  def test_nfl_schedule(self):
    resp = self.api.nfl_schedule(week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('nflSchedule' in json)
    self.assertTrue('matchup' in json['nflSchedule'])
    self.assertTrue(json['nflSchedule']['matchup'])

  def test_player_profile(self):
    resp = self.api.player_profile(self.players)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('playerProfiles' in json)
    self.assertTrue('playerProfile' in json['playerProfiles'])
    self.assertTrue(json['playerProfiles']['playerProfile'])

  def test_player_scores(self):
    resp = self.api.player_scores(self.league_id, week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('playerScores' in json)
    self.assertTrue('playerScore' in json['playerScores'])
    self.assertTrue(json['playerScores']['playerScore'])

  def test_player_status(self):
    resp = self.api.player_status(self.league_id, self.players)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('playerStatuses' in json)
    self.assertTrue('playerStatus' in json['playerStatuses'])
    self.assertTrue(json['playerStatuses']['playerStatus'])

  def test_players(self):
    resp = self.api.players()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('players' in json)
    self.assertTrue('player' in json['players'])
    self.assertTrue(json['players']['player'])

  def test_playoff_brackets(self):
    resp = self.api.playoff_brackets(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('playoffBrackets' in json)
    self.assertTrue('playoffBracket' in json['playoffBrackets'])
    self.assertTrue(json['playoffBrackets']['playoffBracket'])

  def test_points_allowed(self):
    resp = self.api.points_allowed(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('pointsAllowed' in json)
    self.assertTrue('team' in json['pointsAllowed'])
    self.assertTrue(json['pointsAllowed']['team'])

  def test_polls(self):
    resp = self.api.polls(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('polls' in json)
    self.assertTrue('poll' in json['polls'])
    self.assertTrue(json['polls']['poll'])

  def test_pool(self):
    resp = self.api.pool(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('poolPicks' in json)
    self.assertTrue('franchise' in json['poolPicks'])
    self.assertTrue(json['poolPicks']['franchise'])

  def test_projected_scores(self):
    resp = self.api.projected_scores(self.league_id, self.players, week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('projectedScores' in json)
    self.assertTrue('playerScore' in json['projectedScores'])
    self.assertTrue(json['projectedScores']['playerScore'])

  def test_rosters(self):
    resp = self.api.rosters(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('rosters' in json)
    self.assertTrue('franchise' in json['rosters'])
    self.assertTrue(json['rosters']['franchise'])

  def test_rss(self):
    resp = self.api.rss(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('rss' in json)
    self.assertTrue('channel' in json['rss'])
    self.assertTrue(json['rss']['channel'])

  def test_rules(self):
    resp = self.api.rules(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('rules' in json)
    self.assertTrue('positionRules' in json['rules'])
    self.assertTrue(json['rules']['positionRules'])

  def test_salary_adjustments(self):
    resp = self.api.salary_adjustments(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('salaryAdjustments' in json)

  def test_site_news(self):
    resp = self.api.site_news()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('rss' in json)
    self.assertTrue('channel' in json['rss'])
    self.assertTrue(json['rss']['channel'])

  def test_survivor_pool(self):
    resp = self.api.survivor_pool(self.league_id)
    self.assertTrue(resp.ok)

  def test_top_adds(self):
    resp = self.api.top_adds(week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('topAdds' in json)
    self.assertTrue('player' in json['topAdds'])
    self.assertTrue(json['topAdds']['player'])

  def test_top_drops(self):
    resp = self.api.top_drops(week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('topDrops' in json)
    self.assertTrue('player' in json['topDrops'])
    self.assertTrue(json['topDrops']['player'])

  def test_top_owns(self):
    resp = self.api.top_owns(week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('topOwns' in json)
    self.assertTrue('player' in json['topOwns'])
    self.assertTrue(json['topOwns']['player'])

  def test_top_starters(self):
    resp = self.api.top_starters(week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('topStarters' in json)
    self.assertTrue('player' in json['topStarters'])
    self.assertTrue(json['topStarters']['player'])

  def test_trade_bait(self):
    resp = self.api.trade_bait(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('tradeBaits' in json)
    self.assertTrue('tradeBait' in json['tradeBaits'])
    self.assertTrue(json['tradeBaits']['tradeBait'])

  def test_transactions(self):
    resp = self.api.transactions(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('transactions' in json)
    self.assertTrue('transaction' in json['transactions'])
    self.assertTrue(json['transactions']['transaction'])

  def test_weekly_results(self):
    resp = self.api.weekly_results(self.league_id, week=12)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('weeklyResults' in json)
    self.assertTrue('matchup' in json['weeklyResults'])
    self.assertTrue(json['weeklyResults']['matchup'])

  def test_who_should_i_start(self):
    resp = self.api.who_should_i_start()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('whoShouldIStart' in json)
    self.assertTrue('startBenchPair' in json['whoShouldIStart'])
    self.assertTrue(json['whoShouldIStart']['startBenchPair'])

suite = unittest.TestLoader().loadTestsFromTestCase(TestMflApiMethods)
unittest.TextTestRunner(verbosity=2).run(suite)