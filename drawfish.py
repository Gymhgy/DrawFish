import chess
import chess.engine
import sys
import os

def parse_uci(board: chess.Board, msg: str):
    #uci
    if msg == "quit":
        os._exit(0)
    if msg == "uci":
        print("id name DrawFish")
        print("id author Gymhgy & Stockfish authors")
        print("uciok")
        return
    if msg == "ucinewgame":
        return
    if msg == "isready":
        print("readyok")
        return

    if "position startpos moves" in msg:
        moves = msg.split(" ")[3:]
        board.clear()
        board.set_fen(chess.STARTING_FEN)
        for move in moves:
            board.push_uci(move)
        return

    if "position fen" in msg:
        fen = " ".join(msg.split(" ")[2:])
        board.set_fen(fen)
        return

    if msg == "d":
        render(board)
    
    if msg == "play":
        side = chess.WHITE if input("w/b: ") == "w" else chess.BLACK
        if side == chess.WHITE:
            render(board)
            board.push(get_move(board))
        while not board.is_game_over():
            board.push(choose_move(board))
            render(board)
            board.push(get_move(board))

        print(board.result())

    if msg[0:2] == "go":
        tl_str = "wtime" if board.turn == chess.WHITE else "btime"
        inc_str = "winc" if board.turn == chess.WHITE else "binc"
        split = msg.split()
        time_left = None
        increment = None
        if tl_str in split:
            try:
                time_left = int(split[split.index(tl_str) + 1])
            except IndexError:
                time_left = None
        if inc_str in split:
            try:
                increment = int(split[split.index(inc_str) + 1])
            except IndexError:
                increment = None

        move = choose_move(board, time_left, increment)

        print("bestmove %s" % move.uci())

def get_move(board):
    move = board.parse_san(input("> "))
    if move in board.legal_moves:
        return move
    else:
        return get_move(board)

def render(board):
    print(board)

def manage_time(time_left, increment, num_legal_moves) -> chess.engine.Limit:
    if increment == None:
        increment = 0
    total = (increment + 0.05 * time_left)/1000
    return chess.engine.Limit(time = total/num_legal_moves)
    

def choose_move(board, time_left = None, increment = None):
    chosen = chess.Move.null
    chosen_score = 100001
    print(time_left, increment)
    limit = chess.engine.Limit(time = 0.1) if time_left == None else manage_time(time_left, increment, len(list(board.legal_moves)))
    print(limit)
    for move in board.legal_moves:
        board.push(move)
        info = engine.analyse(board, limit)
        score = abs(info["score"].relative.score(mate_score = 100000))
        if score < chosen_score:
            chosen = move
            chosen_score = score
        board.pop()

    return chosen

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_13_win_x64_bmi2\\stockfish13.exe")
    while True:
        msg = input()
        parse_uci(board, msg)
    pass