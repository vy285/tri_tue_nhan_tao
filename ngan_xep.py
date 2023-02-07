from moi_truong import *

class Stack :
    def __init__(self):
        self.nodes = []
        self.frontier = set()
    
    def __eq__(self,other):
        return self.nodes == other.nodes
    
    def empty(self):
        return len(self.nodes) == 0
    
    def add(self, node : Node):
        if not isinstance(node, Node):
            raise TypeError(" khong dung kieu du lieu")
        self.nodes.append(node)

    def remove(self):
        if self.empty():
            raise ValueError("ngan xep rong")
        node = self.nodes[-1]
        self.nodes.pop()
        return node