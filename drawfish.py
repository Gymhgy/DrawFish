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
        move = choose_move(board)
        print("bestmove %s" % move.uci())

def get_move(board):
    move = board.parse_san(input("> "))
    if move in board.legal_moves:
        return move
    else:
        return get_move(board)

def render(board):
    print(board)

def choose_move(board):
    chosen = chess.Move.null
    chosen_score = 100001
    for move in board.legal_moves:
        board.push(move)
        #1 million nodes
        info = engine.analyse(board, chess.engine.Limit(time = 0.2))
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