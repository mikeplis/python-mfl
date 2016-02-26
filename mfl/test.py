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

  def test_players(self):
    resp = self.api.players()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue('players' in json)
    self.assertTrue('player' in json['players'])
    self.assertTrue(json['players']['player'])

  def test_all_rules(self):
    resp = self.api.all_rules()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_injuries(self):
    resp = self.api.injuries()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_nfl_schedule(self):
    resp = self.api.nfl_schedule()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_adp(self):
    resp = self.api.adp()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_aav(self):
    resp = self.api.aav()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_top_adds(self):
    resp = self.api.top_adds()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_top_drops(self):
    resp = self.api.top_drops()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_top_starters(self):
    resp = self.api.top_starters()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_top_owns(self):
    resp = self.api.top_owns()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_league(self):
    resp = self.api.league(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_rules(self):
    resp = self.api.rules(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_rosters(self):
    resp = self.api.rosters(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_league_standings(self):
    resp = self.api.league_standings(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_weekly_results(self):
    resp = self.api.weekly_results(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_live_scoring(self):
    resp = self.api.live_scoring(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_player_scores(self):
    resp = self.api.player_scores(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_draft_results(self):
    resp = self.api.draft_results(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_future_draft_picks(self):
    resp = self.api.future_draft_picks(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_auction_results(self):
    resp = self.api.auction_results(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_free_agents(self):
    resp = self.api.free_agents(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_transactions(self):
    resp = self.api.transactions(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_rss(self):
    resp = self.api.rss(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_site_news(self):
    resp = self.api.site_news()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_projected_scores(self):
    resp = self.api.projected_scores(self.league_id, self.players)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_league_search(self):
    resp = self.api.league_search('asdf')
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_message_board(self):
    resp = self.api.message_board(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_message_board_thread(self):
    resp = self.api.message_board_thread(self.league_id, 3571222)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_player_profile(self):
    resp = self.api.player_profile(self.players)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_player_status(self):
    resp = self.api.player_status(self.league_id, self.players)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_accounting(self):
    resp = self.api.accounting(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_calendar(self):
    resp = self.api.calendar(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_points_allowed(self):
    resp = self.api.points_allowed(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_trade_bait(self):
    resp = self.api.trade_bait(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_who_should_i_start(self):
    resp = self.api.who_should_i_start()
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_polls(self):
    resp = self.api.polls(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_survivor_pool(self):
    resp = self.api.survivor_pool(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_pool(self):
    resp = self.api.pool(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_playoff_brackets(self):
    resp = self.api.playoff_brackets(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_appearance(self):
    resp = self.api.appearance(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_tradeable_assets(self):
    resp = self.api.tradeable_assets(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)

  def test_salary_adjustments(self):
    resp = self.api.salary_adjustments(self.league_id)
    self.assertTrue(resp.ok)

    json = resp.json()
    self.assertTrue(True)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMflApiMethods)
unittest.TextTestRunner(verbosity=2).run(suite)