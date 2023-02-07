import time
import random
from moi_truong import *
"""
    
"""
DELAY = 0.01
class Maze :
    def __init__(self,board:Board):
        self.board =board

    def initialize(self):
        pass

    def get_frontiers(self,state :tuple) ->set:
        pass

    def frontier_neighbor(self,frontier:tuple) ->tuple:
        pass

    def connect_cell(self,cell_1:tuple , cell_2:tuple):
        pass

    def generate(self) :
        pass