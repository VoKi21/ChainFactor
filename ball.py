class Ball:
    def __init__(self, value, protected):
        self.value = value
        self.protection = 2 if protected else 0
        self.to_remove = False
