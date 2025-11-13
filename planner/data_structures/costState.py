class CostState:
    def __init__(self, g, parent = None, action = None):
            self.g = g
            self.parent = parent
            self.action = action