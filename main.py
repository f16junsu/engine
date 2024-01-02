'''
Pre
'''


from stockfish import Stockfish
stockfish = Stockfish(depth=35)
print("Stockfish ver: ", stockfish._stockfish_major_version)

import chess
import chess.pgn
import random
from pprint import pprint
import numpy as np
import os
import glob
import time


# check if the position(@board) is game over
def checkEndCondition(board) -> bool:
    if (board.is_checkmate()):
        print("Game over by checkmate")
        return True
    elif (board.is_stalemate()):
        print("Game over by stalemate")
        return True
    elif (board.is_insufficient_material()):
        print("Game over by insufficient material")
        return True
    elif (board.can_claim_threefold_repetition()):
        print("Game over by three-fold repetition")
        return True
    elif (board.can_claim_fifty_moves()):
        print("Game over by fifty moves")
        return True
    elif (board.can_claim_draw()):
        print("Game over by draw")
        return True
    return False

class Game:
    def __init__(self, num = 0):
        print("Engine Game Generator")
        self.count = num
        self.MAX_MOVES = 500


    # main game generating method
    def mineGames(self, gameMode = 0):
        self.count += 1
        print("------ Game: ", self.count, "------")
        game = chess.pgn.Game()
        node = game
        board = chess.Board()
        currentGameMoves = []
        game.headers["Event"] = f"Game{self.count}"
        game.headers["White"] = f"Stockfish {stockfish._stockfish_major_version}"
        game.headers["Black"] = f"Stockfish {stockfish._stockfish_major_version}"
        stockfish.set_position([])

        # Mode 0. Generates a game with engine search time 1s, max depth 25
        if gameMode == 0:
            print("Mode 0 : engine search time 1000ms")
            print("Start position:")
            print(board)
            for j in range(self.MAX_MOVES):
                move = stockfish.get_best_move_time(1000)
                node = node.add_variation(chess.Move.from_uci(move))
                board.push_san(move)
                currentGameMoves.append(move)
                stockfish.set_position(currentGameMoves)
                if board.is_game_over():
                    print("Game over")
                    break

        # Mode 1. Can select engine search time in ms.
        elif gameMode == 1:
            print("Mode 1")
            search_time = int(input("Enter engine search time (in ms unit): "))
            print("Start position:")
            print(board)
            for j in range(self.MAX_MOVES):
                move = stockfish.get_best_move_time(search_time)
                node = node.add_variation(chess.Move.from_uci(move))
                board.push_san(move)
                currentGameMoves.append(move)
                stockfish.set_position(currentGameMoves)
                if board.is_game_over():
                    print("Game over")
                    break

        # Mode 2. Generate a game by randomly choosing a move from the
        # top or the second top move in the opening(first 5 moves). Ratio is 70 : 30
        elif gameMode == 2:
            print("Mode 2")
            print("Start position:")
            print(board)
            stockfish.set_depth(25)
            for j in range(self.MAX_MOVES):
                move = str()
                if j < 10:
                    moves = stockfish.get_top_moves(2)
                    if len(moves) == 0:
                        print("game over")
                        break
                    elif len(moves) == 1:
                        move = moves[0]["Move"]
                    else:
                        move = random.choices(moves, weights=(70, 30), k=1)[0]["Move"]
                        for d in moves:
                            if d["Mate"] == 1:
                                move = d["Move"]
                    continue
                stockfish.set_depth(35)
                move = stockfish.get_best_move_time(2000)
                node = node.add_variation(chess.Move.from_uci(move))
                board.push_san(move)
                currentGameMoves.append(move)
                stockfish.set_position(currentGameMoves)
                if board.is_game_over():
                    print("Game over")
                    stockfish.set_depth(35)
                    break
        else:
            print("Unexpected behavior. Game not generated")
            return
        print(game, file=open(f"data/game{self.count}.pgn", "w"), end = "\n\n")


def main_routine():
    generator = Game(2)
    while True:
        mode = int(input("Input game mode: "))
        if mode > 2:
            break
        else:
            generator.mineGames(mode)



### main ###
main_routine()