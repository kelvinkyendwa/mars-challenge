class Mars(object):
    """
     creates a Mars map
    """

    def __init__(self, x, y):
        """
        Init
        """
        self.x = x
        self.y = y
        self.occupied = []
