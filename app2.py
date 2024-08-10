"""from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'''
          ##         .
    ## ## ##        ==
 ## ## ## ## ##    ===
/\___/ ===
{                       /  ===-
\______ O           __/
 \    \         __/
  \____\_______/


Hello from Docker!
''')

def run():
    print('Starting server...')
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server started!')
    httpd.serve_forever()

if __name__ == '__main__':
    run()"""
"""
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize the Tic-Tac-Toe board
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

def check_win(mark):
    for i in range(3):
        if all([board[i][j] == mark for j in range(3)]) or all([board[j][i] == mark for j in range(3)]):
            return True
    if all([board[i][i] == mark for i in range(3)]) or all([board[i][2 - i] == mark for i in range(3)]):
        return True
    return False

def check_draw():
    return all([cell != ' ' for row in board for cell in row])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player
    data = request.json
    row = data['row']
    col = data['col']

    if board[row][col] == ' ':
        board[row][col] = current_player

        if check_win(current_player):
            winner = current_player
            board_reset()
            return jsonify({'status': 'win', 'winner': winner})

        if check_draw():
            board_reset()
            return jsonify({'status': 'draw'})

        current_player = 'O' if current_player == 'X' else 'X'
        return jsonify({'status': 'continue', 'next_player': current_player, 'board': board})
    else:
        return jsonify({'status': 'invalid'})

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board': board})

def board_reset():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)"""
