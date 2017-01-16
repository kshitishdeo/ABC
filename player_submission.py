#!/usr/bin/env python

# This file is your main submission that will be graded against. Only copy-paste
# code on the relevant classes included here from the IPython notebook. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.

# Submission Class 1
class OpenMoveEvalFn():
    """Evaluation function that outputs a 
    score equal to how many moves are open
    for your computer player on the board."""
    def score(self, game, maximizing_player_turn=True):
        a=0
        dict1 = game.get_legal_moves()
        for i in dict1:
            for j in dict1[i]:
                a=a+1;
        dict2= game.get_opponent_moves()
        return a-len(dict2)

class CustomPlayer():
    # TODO: finish this class!
    """Player that chooses a move using 
    your evaluation function and 
    a depth-limited minimax algorithm 
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move
    in less than 1000 milliseconds."""
    def __init__(self,  search_depth=3, eval_fn=OpenMoveEvalFn()):
        # if you find yourself with a superior eval function, update the
        # default value of `eval_fn` to `CustomEvalFn()`
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        
    def opponent_eval(self,game):
        a=0
        dict1 = game.get_legal_moves()
        for i in dict1:
            for j in dict1[i]:
                a=a+1;
        dict2= game.get_opponent_moves()
        return len(dict2)-a
    
    def move(self, game, legal_moves, time_left):
        best_move,best_queen, utility = self.alphabeta(game,time_left, depth=self.search_depth) # queen added as return type
      
        return best_move, best_queen # queen added as return type


    def utility(self, game, maximizing):
        legal_moves=game.get_legal_moves()
        if maximizing:
            if not game.get_opponent_moves():
                return float("inf")
            if (not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__])):
                return float("-inf")

            return self.eval_fn.score(game)

        else:
            if (not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__])):
                return float("inf")
            if not game.get_opponent_moves():
                return float("-inf")

            return self.opponent_eval(game)


    def minimax(self, game, time_left, depth=float("inf"), maximizing_player=True):
        legal_moves = game.get_legal_moves()
        if not depth or (not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__])): #to change legal move
            return None, None, self.utility(game, maximizing_player)

        if maximizing_player:
            best_move = None
            best_queen = None
            best_val =  float("-inf")
            for queen in legal_moves:
                for move in legal_moves[queen]:
                    _,_, val = self.minimax(game.forecast_move(move,queen), time_left, depth -1, False )
                    if val > best_val:
                        best_val = val
                        best_move = move
                        best_queen = queen

        else:
            best_move = None
            best_queen = None
            best_val = float("inf")
            for queen in legal_moves:
                for move in legal_moves[queen]:
                    _,_, val = self.minimax(game.forecast_move(move,queen), time_left, depth -1, True)
                    if val < best_val:
                        best_val = val
                        best_move = move
                        best_queen = queen

        return best_move,best_queen, best_val

    def alphabeta(self, game, time_left, depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        legal_moves = game.get_legal_moves()

        if not depth or (not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__])): #to change legal move
            return None, None, self.utility(game, maximizing_player)

        if maximizing_player:
            val = float("-inf")
            best_move = None
            best_queen = None
            for queen in legal_moves:
                for move in legal_moves[queen]:
                    node = game.forecast_move(move,queen)
                    _,_, new_val = self.alphabeta(node, time_left, depth-1, alpha, beta, False)

                    if new_val > val:
                        val = new_val
                        best_move = move
                        best_queen = queen
                    alpha = max( alpha, val)

                    if beta <= alpha:
                        return best_move,best_queen, beta
            return best_move,best_queen, val

        else:
            val = float("inf")
            best_move = None
            best_queen = None
            for queen in legal_moves:
                for move in legal_moves[queen]:
                    node = game.forecast_move(move,queen)
                    _,_, new_val = self.alphabeta(node, time_left, depth -1 , alpha, beta, True)

                    if new_val < val:
                        val = new_val
                        best_move = move
                        best_queen = queen
                    beta = min(beta, val)

                    if beta <= alpha:
                        return best_move,best_queen, alpha

            return best_move, best_queen, val

