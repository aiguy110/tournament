class Tournament():
    def __init__(self, player_list):
        self.player_list = player_list
        self.winner_record = {}
        self.loser_record = {}

        self.game_dict = {}
        self._gen_games(self.player_list)

    def _gen_games(self, player_list):
        need_to_play = player_list[:]
        game_counter = 1
        while len(need_to_play) != 1 :
            p1 = need_to_play.pop(0)
            p2 = need_to_play.pop(0)
            game_id = 'game'+str(game_counter)
            self.game_dict[game_id] = (p1, p2)
            game_counter += 1
            need_to_play.insert(len(need_to_play), game_id)

    def getNames(self, game_id):
        try:
            p1, p2 = self.game_dict[game_id]
            if p1 in self.winner_record:
                p1 = self.winner_record[p1]
            elif p1[:4] == 'game':
                p1 = '[Winner of {}]'.format(p1)

            if p2 in self.winner_record:
                p2 = self.winner_record[p2]
            elif p2[:4] == 'game':
                p2 = '[Winner of {}]'.format(p2)

            return (p1, p2)
        except:
            return None


    def getPlayers(self, game_id):
        if game_id not in self.game_dict:
            return None

        maybe_players = list(self.game_dict[game_id])
        for p in range(len(maybe_players)):
            while maybe_players[p] not in self.player_list:
                maybe_players[p] = self.winner_record[maybe_players[p]]

        return maybe_players # definitely now

    def setWinner(self, game_id, player):
        self.winner_record[game_id] = player
        both_players = self.getPlayers(game_id)
        both_players.remove(player)
        self.loser_record[game_id] = both_players[0]

    def hasLost(self, player):
        return player in self.loser_record.values()


    def getNextUnplayedGame(self, exclude_games):
        """ Returns the name of the next unplayed game, or None if all games have recorded winners"""
        game_counter = 1
        while 'game{}'.format(game_counter) in self.winner_record or 'game{}'.format(game_counter) in exclude_games:
            game_counter += 1

        if 'game{}'.format(game_counter) in self.game_dict:
            return 'game{}'.format(game_counter)
        else:
            return None
