from flask import Flask, jsonify, render_template, request
from tournament import Tournament
from threading import Thread


player_list = []
with open('players.txt', 'r') as f:
    for line in f:
        player_list.append(line.strip())
t = Tournament(player_list)
play_status = {'table1': 'game1', 'table2':'game2', 'next_up': 'game3'}


app = Flask(__name__)

@app.route('/_get_status')
def get_status():
    pretty_status = {}
    for key in play_status:
        pretty_status[key] = t.getGameString(play_status[key])
    return jsonify(pretty_status)

@app.route('/')
def index():
    return render_template('index.html')

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
