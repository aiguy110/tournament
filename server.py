from flask import Flask, jsonify, render_template, send_from_directory, redirect, request
from tournament import Tournament
from threading import Thread


player_list = []
with open('players.txt', 'r') as f:
    for line in f:
        player_list.append(line.strip())
t = Tournament(player_list)

# This defines the format and is immedeately over written
play_status = {
                'table1': {'game_id': 'game1', 'players': ['Player1', 'Player2']},
                'table2': {'game_id': 'game2', 'players': ['Player3', 'Player4']},
                'next_up': {'game_id': 'game3', 'text':'[Winner of game1] vs. [Winner of game2]'},
                'players': player_list
               }
def update_play_status(tournament, table_winner=None):
    if table_winner != None and table_winner != 'no_winner':
        try:
            table_id, winner_num = table_winner
            winner_id = play_status[table_id]['players'][winner_num]
            tournament.setWinner(play_status[table_id]['game_id'], winner_id)
            new_game = t.getNextUnplayedGame(exclude_games=[play_status['table1']['game_id'], play_status['table2']['game_id']])
            play_status[table_id] = {
                'game_id': new_game,
                'players': t.getNames(new_game)
            }
        except:
            new_game = {'game_id': 'no_game', 'players':None}
            play_status[table_id] = {
                'game_id': new_game,
                'players': None
            }

    for table in ['table1', 'table2']:
        play_status[table]['players'] = t.getNames(play_status[table]['game_id'])

    on_deck = t.getNextUnplayedGame(exclude_games=[play_status['table1']['game_id'], play_status['table2']['game_id']])
    if on_deck is not None:
        player_names = t.getNames(on_deck)
        play_status['next_up'] = {'game_id':on_deck, 'text': '{} vs. {}'.format(player_names[0], player_names[1])}
    else:
        play_status['next_up'] = {'game_id':on_deck, 'text': ''}

update_play_status(t)


app = Flask(__name__)

@app.route('/_update_status')
def update_status():
    data = request.args['button'] #e.g. "t1p2" (for table1 player2)

    if data != 'no_winner':
        table_str = {'t1':'table1', 't2':'table2'}[data[:2]]
        game_str = play_status[table_str]
        p_index = int(data[3])-1

        # Update the tournament object and the json-like object
        update_play_status(t, table_winner=(table_str, p_index))

    return jsonify(play_status)



    pretty_status = {}
    for key in play_status:
        pretty_status[key] = t.getGameString(play_status[key])
    return jsonify(pretty_status)

@app.route('/')
def root():
    return redirect("/index.html", code=302)

@app.route('/<path:path>')
def index(path):
    return send_from_directory('static/', path)

server_thread = Thread(target=app.run)
server_thread.start()

if __name__ == '__main__':
    while True:
        cmdline = input('>')
        words = cmdline.split(' ')
        if words[0] == 'winner':
            if words[1] in ['table1', 'table2']:
                t.setWinner(play_status[words[1]], words[2])
                play_status[words[1]] = t.getNextUnplayedGame(exclude_games=[play_status['table1'], play_status['table2']])
                play_status['next_up'] = t.getNextUnplayedGame(exclude_games=[play_status['table1'], play_status['table2']])

        elif words[0] == 'show':
            print('table1: {}'.format(play_status['table1']))
            print('table2: {}'.format(play_status['table2']))
            print('next_up: {}'.format(play_status['next_up']))

            print('')

            for g in range(len(t.game_dict)):
                print(t.getGameString('game'+str(g+1)))

        elif words[0] == 'exit':
            break
