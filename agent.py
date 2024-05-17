import copy


class Board:
    def __init__(self):
        self.board = self.create_board()

    def put(self, pos, color):
        x, y = pos
        self.board[x][y] = color

    def create_board(self):
        return [['     ' for _ in range(8)] for _ in range(8)]

    def move(self, move):
        (start_x, start_y), (end_x, end_y) = move
        piece = self.board[start_x][start_y]
        self.board[start_x][start_y] = '     '
        self.board[end_x][end_y] = piece

    def is_inBounds(self, pos):
        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8

    def get_position(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)
        print()


class Agent:
    def __init__(self, color):
        self.color = color

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.is_game_over(board):
            return self.heuristic(board)
        # turn of max player
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_moves(board, self.color):
                new_board = copy.deepcopy(board)
                new_board.move(move)
                eval = self.minimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move if depth == 3 else max_eval
        # turn of min player
        else:
            min_eval = float('inf')
            opponent_color = 'black' if self.color == 'white' else 'white'
            for move in self.get_moves(board, opponent_color):
                new_board = copy.deepcopy(board)
                new_board.move(move)
                eval = self.minimax(new_board, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
            return min_eval

    def heuristic(self, board):
        white_score = 0
        black_score = 0

        for x in range(8):
            for y in range(8):
                if board.board[x][y] == 'white':
                    # how mauch it is close to the end is better
                    white_score += (7 - x)
                elif board.board[x][y] == 'black':
                    black_score += x  # how much it is close to the end is better

        return white_score - black_score if self.color == 'white' else black_score - white_score

    def is_game_over(self, board):
        # if white pawn has reached (0,y)
        for y in range(8):
            if board.board[0][y] == 'white':
                return True

        # if black pawn has reached (7,y)
        for y in range(8):
            if board.board[7][y] == 'black':
                return True

        # if both pwans block each other
        if not self.get_moves(board, 'white') and not self.get_moves(board, 'black'):
            return True

        return False

    def get_moves(self, board, color):
        moves = []
        direction = -1 if color == 'white' else 1

        for x in range(8):
            for y in range(8):
                if board.board[x][y] == color:
                    # move stright
                    new_x = x + direction
                    if board.is_inBounds((new_x, y)) and board.board[new_x][y] == '     ':
                        moves.append([(x, y), (new_x, y)])

                    # remove opponenet pawn diagonal
                    for new_y in [y - 1, y + 1]:
                        if board.is_inBounds((new_x, new_y)) and board.board[new_x][new_y] not in ['     ', color]:
                            moves.append([(x, y), (new_x, new_y)])

        return moves


board = None
agent = None


def setup(position):
    global board, agent
    board = Board()
    white_pawns = position["white"]
    for pawn in white_pawns:
        board.put(pawn, "white")

    black_pawns = position["black"]
    for pawn in black_pawns:
        board.put(pawn, "black")

    agent = Agent(position["color"])


def move(previous_move):
    # first we assume the the turn is belong to max player
    if previous_move != None:
        board.move(previous_move)
    best_move = agent.minimax(board, 3, True)
    # print(best_move)
    board.move(best_move)
    return best_move


initial_position = {
    "white": [[5, 0], (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)],
    "black": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
    "color": 'white'
}

setup(initial_position)
while not agent.is_game_over(board):
    board.print_board()
    sx = int(input())
    sy = int(input())
    ex = int(input())
    ey = int(input())
    pv = [(sx, sy), (ex, ey)]
    move(pv)
# board.print_board()
# m = move([(6, 0), (5, 0)])
# print(m)

# board.print_board()
# print(agent.is_game_over(board))
