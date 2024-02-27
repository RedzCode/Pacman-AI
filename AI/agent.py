from collections import deque #Deque (Doubly Ended Queue)
import torch
import random
import numpy as np
from Pacman_game.AiPacman import PacmanGame, Pos
from Pacman_game.utils import Direction

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 #Learning rate

class Agent():
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # control randomness
        self.gamma = 0 # discount rate
        #if we exceed the memory it will automatically remove element from the left => popleft()
        self.memory = deque(maxlen=MAX_MEMORY) 
        #TODO : model, trainer
        
    
    def get_state(self, game):
        pass
    
    def remember(self, state, action, reward, next_state, done):
        pass
    
    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        pass
    
    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0 #bestScore = 0
    
    agent = Agent()
    game = PacmanGame()
    
    while True: 
        state_old = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        score, game_over, game_won, reward = game.play_action(final_move)
        
        state_new = agent.get_state(game)
        
        # train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        
        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over : 
            # train long memory
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                #agent.model.save()
                            
            print('Game: ', agent.n_games, 'Score: ', score, 'Record: ', record)
            
            # TODO : plot