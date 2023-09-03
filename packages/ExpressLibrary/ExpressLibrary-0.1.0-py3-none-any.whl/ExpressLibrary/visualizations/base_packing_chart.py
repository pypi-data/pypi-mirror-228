class BasePackingChart:
    def __init__(self, data, title=None):
        self.data = data
        self.title = title

    def validate_data(self):
        pass

    def render(self):
        raise NotImplementedError("The render method must be implemented in the subclass.")
