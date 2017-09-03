from flask import Flask, jsonify, render_template, request
from tournament import Tournament
from threading import Thread

app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')

server_thread = Thread(target=app.run)
server_thread.start()

if __name__ == '__main__':
    player_list = []
    with open('players.txt', 'r') as f:
        for line in f:
            player_list.append(line.strip())

    t = Tournament(player_list)
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
