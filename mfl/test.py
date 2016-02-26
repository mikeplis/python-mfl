import unittest
from api import Api

class TestMflApiMethods(unittest.TestCase):
  def setUp(self):
    self.api = Api(2015)
    self.league_id = 35465
    self.players = [7260, 6997]

  def test_players(self):
    self.api.players()

  def test_all_rules(self):
    self.api.all_rules()

  def test_injuries(self):
    self.api.injuries()

  def test_nfl_schedule(self):
    self.api.nfl_schedule()

  def test_adp(self):
    self.api.adp()

  def test_aav(self):
    self.api.aav()

  def test_top_adds(self):
    self.api.top_adds()

  def test_top_drops(self):
    self.api.top_drops()

  def test_top_starters(self):
    self.api.top_starters()

  def test_top_owns(self):
    self.api.top_owns()

  def test_league(self):
    self.api.league(self.league_id)

  def test_rules(self):
    self.api.rules(self.league_id)

  def test_rosters(self):
    self.api.rosters(self.league_id)

  def test_league_standings(self):
    self.api.league_standings(self.league_id)

  def test_weekly_results(self):
    self.api.weekly_results(self.league_id)

  def test_live_scoring(self):
    self.api.live_scoring(self.league_id)

  def test_player_scores(self):
    self.api.player_scores(self.league_id)

  def test_draft_results(self):
    self.api.draft_results(self.league_id)

  def test_future_draft_picks(self):
    self.api.future_draft_picks(self.league_id)

  def test_auction_results(self):
    self.api.auction_results(self.league_id)

  def test_free_agents(self):
    self.api.free_agents(self.league_id)

  def test_transactions(self):
    self.api.transactions(self.league_id)

  def test_rss(self):
    self.api.rss(self.league_id)

  def test_site_news(self):
    self.api.site_news()

  def test_projected_scores(self):
    self.api.projected_scores(self.league_id, self.players)

  def test_league_search(self):
    self.api.league_search('asdf')

  def test_message_board(self):
    self.api.message_board(self.league_id)

  def test_message_board_thread(self):
    self.api.message_board_thread(self.league_id, 3571222)

  def test_player_profile(self):
    self.api.player_profile(self.players)

  def test_player_status(self):
    self.api.player_status(self.league_id, self.players)

  def test_accounting(self):
    self.api.accounting(self.league_id)

  def test_calendar(self):
    self.api.calendar(self.league_id)

  def test_points_allowed(self):
    self.api.points_allowed(self.league_id)

  def test_trade_bait(self):
    self.api.trade_bait(self.league_id)

  def test_who_should_i_start(self):
    self.api.who_should_i_start()

  def test_polls(self):
    self.api.polls(self.league_id)

  def test_survivor_pool(self):
    self.api.survivor_pool(self.league_id)

  def test_pool(self):
    self.api.pool(self.league_id)

  def test_playoff_brackets(self):
    self.api.playoff_brackets(self.league_id)

  def test_appearance(self):
    self.api.appearance(self.league_id)

  def test_tradeable_assets(self):
    self.api.tradeable_assets(self.league_id)

  def test_salary_adjustments(self):
    self.api.salary_adjustments(self.league_id)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMflApiMethods)
unittest.TextTestRunner(verbosity=2).run(suite)