class Movement():
    def __init__(self, time, movement):
        self.time = time
        self.movement = movement
    
    def __str__(self):
        return f'tiempo: {self.time}, mov: {self.movement}'
