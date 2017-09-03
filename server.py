from flask import Flask, jsonify, render_template, request
from tournament import Tournament
from threading import Thread


player_list = []
with open('players.txt', 'r') as f:
    for line in f:
        player_list.append(line.strip())
t = Tournament(player_list)
play_status = {'table1': 'game1', 'table2':' game2', 'next_up': 'game3'}


app = Flask(__name__)

@app.route('/_get_status')
def add_numbers():
    return jsonify(play_status)

@app.route('/')
def index():
    return render_template('index.html')

server_thread = Thread(target=app.run)
server_thread.start()

if __name__ == '__main__':
    while True:
        cmd = input('>')
        words = cmd.split(' ')
        if words[0] == 'winner':
            t.setWinner(words[1], words[2])
        if words[0] == 'show':
            next_game = t.getNextUnplayedGame()
            print(t.getGameString(next_game))
        if words[0] == 'exit':
            break
