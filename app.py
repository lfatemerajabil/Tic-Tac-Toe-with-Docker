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
    run()


from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Initialize the game board and current player
game_board = [' ' for _ in range(9)]
current_player = 'X'

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_player

        # Extract query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        if 'cell' in query_components:
            cell = int(query_components['cell'][0])
            if game_board[cell] == ' ':
                game_board[cell] = current_player  # Set the current player's move
                if not self.check_win():
                    self.switch_player()  # Switch turns
            self.send_board()
        else:
            self.send_board()

    def send_board(self):
        # Send the Tic-Tac-Toe page with the current board
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(self.generate_html(), 'utf-8'))

    def generate_html(self):
        # Generate the HTML for the Tic-Tac-Toe board
        board_html = "<table border='1' style='margin: 0 auto;'>"
        for i in range(3):
            board_html += "<tr>"
            for j in range(3):
                cell_index = i * 3 + j
                cell_value = game_board[cell_index]
                board_html += f"<td style='width:60px;height:60px;text-align:center;font-size:24px'>"
                if cell_value == ' ':
                    board_html += f"<a href='/?cell={cell_index}'>{cell_value}</a>"
                else:
                    board_html += cell_value
                board_html += "</td>"
            board_html += "</tr>"
        board_html += "</table>"

        return f'''
            <html>
            <head>
                <title>Tic-Tac-Toe</title>
            </head>
            <body style="text-align: center; padding-top: 50px;">
                <h1>Tic-Tac-Toe</h1>
                <h2>Current Player: {current_player}</h2>
                {board_html}
                <br><br>
                <a href="/">Restart Game</a>
            </body>
            </html>
        '''

    def switch_player(self):
        # Switch the current player between 'X' and 'O'
        global current_player
        current_player = 'O' if current_player == 'X' else 'X'

    def check_win(self):
        # Check for a winning combination
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in winning_combinations:
            if game_board[combo[0]] == game_board[combo[1]] == game_board[combo[2]] != ' ':
                self.send_win_message(game_board[combo[0]])
                return True
        return False

    def send_win_message(self, winner):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(f"<html><body style='text-align: center; padding-top: 50px;'><h1>{winner} wins!</h1></body></html>", 'utf-8'))
        self.wfile.write(bytes('<a href="/">Play again</a>', 'utf-8'))
        global game_board, current_player
        game_board = [' ' for _ in range(9)]  # Reset the board
        current_player = 'X'  # Reset the current player

def run():
    print('Starting server...')
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server started on port 8080!')
    httpd.serve_forever()

if __name__ == '__main__':
    run()


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
    app.run(host='0.0.0.0', port=5000)

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Define the number to sum with
PREDEFINED_NUMBER = 10

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Check if 'number' parameter is in the query
        if 'number' in query_components:
            try:
                # Get the number from the query parameter
                user_number = int(query_components['number'][0])
                # Calculate the sum
                result = user_number + PREDEFINED_NUMBER
                # Generate the response
                response = f'''
                    <html>
                    <head><title>Sum Result</title></head>
                    <body style="text-align: center; padding-top: 50px;">
                        <h1>Sum Result</h1>
                        <p>You entered: {user_number}</p>
                        <p>Sum with {PREDEFINED_NUMBER}: {result}</p>
                        <br>
                        <a href="/">Go Back</a>
                    </body>
                    </html>
                '''
            except ValueError:
                # Handle the case where the input is not a valid integer
                response = '''
                    <html>
                    <head><title>Error</title></head>
                    <body style="text-align: center; padding-top: 50px;">
                        <h1>Error</h1>
                        <p>Invalid input. Please provide a valid number.</p>
                        <br>
                        <a href="/">Go Back</a>
                    </body>
                    </html>
                '''
        else:
            # Provide a form for the user to input a number
            response = '''
                <html>
                <head><title>Enter Number</title></head>
                <body style="text-align: center; padding-top: 50px;">
                    <h1>Enter a Number</h1>
                    <form action="/" method="get">
                        <input type="number" name="number" required>
                        <input type="submit" value="Submit">
                    </form>
                </body>
                </html>
            '''

        # Send the response to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

def run():
    print('Starting server...')
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server started on port 8080!')
    httpd.serve_forever()

if __name__ == '__main__':
    run()"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Initialize the game board and current player
game_board = [' ' for _ in range(9)]
current_player = 'X'
game_over = False
winner = None
status_message = ''

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_player, game_board, game_over, winner, status_message

        # Extract query parameters from the URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Handle game reset
        if 'action' in query_components and query_components['action'][0] == 'restart':
            self.reset_game()
            self.send_board()
            return

        # Handle cell clicks
        if 'cell' in query_components:
            cell = int(query_components['cell'][0])
            if not game_over and game_board[cell] == ' ':
                game_board[cell] = current_player  # Update the board with the current player's move
                if not self.check_win():  # Check if the move resulted in a win
                    self.switch_player()  # Switch to the next player
                else:
                    game_over = True  # Set the game as over when a win is detected
            self.send_board()
        else:
            self.send_board()

    def send_board(self):
        # Send the Tic-Tac-Toe board HTML page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(self.generate_html(), 'utf-8'))

    def generate_html(self):
        # Generate the HTML for the Tic-Tac-Toe board
        board_html = "<table border='1' style='margin: 0 auto; border-collapse: collapse;'>"
        for i in range(3):
            board_html += "<tr>"
            for j in range(3):
                cell_index = i * 3 + j
                cell_value = game_board[cell_index]
                cell_style = 'width:60px;height:60px;text-align:center;font-size:24px;'
                if not game_over and cell_value == ' ':
                    board_html += f"<td style='{cell_style}'><a href='/?cell={cell_index}' style='display:block;height:100%;width:100%;text-decoration:none;color:black;'>&nbsp;</a></td>"
                else:
                    board_html += f"<td style='{cell_style}'>{cell_value}</td>"
            board_html += "</tr>"
        board_html += "</table>"

        # Generate the game status message
        status_message = ""
        if game_over and winner:
            status_message = f"<h2>{winner} wins!</h2>"
        elif game_over and winner is None:
            status_message = "<h2>It's a draw!</h2>"

        restart_link = '<a href="/?action=restart">Restart Game</a>'
        return f'''
            <html>
            <head>
                <title>Tic-Tac-Toe</title>
            </head>
            <body style="text-align: center; padding-top: 50px;">
                <h1>Tic-Tac-Toe</h1>
                <h2>Current Player: {current_player}</h2>
                {status_message}
                {board_html}
                <br><br>
                {restart_link}
            </body>
            </html>
        '''

    def switch_player(self):
        # Switch the current player between 'X' and 'O'
        global current_player
        current_player = 'O' if current_player == 'X' else 'X'

    def check_win(self):
        # Check for a winning combination
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in winning_combinations:
            if game_board[combo[0]] == game_board[combo[1]] == game_board[combo[2]] != ' ':
                global winner
                winner = game_board[combo[0]]  # Set the winner
                return True
        # Check for a draw (if no empty cells left)
        if all(cell != ' ' for cell in game_board):
            global status_message
            status_message = "<h2>It's a draw!</h2>"
            return True
        
        return False

    def reset_game(self):
        # Reset the game board, current player, and game state
        global game_board, current_player, game_over, winner, status_message
        game_board = [' ' for _ in range(9)]
        current_player = 'X'
        game_over = False
        status_message = ""
        winner = None

def run():
    print('Starting server...')
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server started on port 8080!')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
