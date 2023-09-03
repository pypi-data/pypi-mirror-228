class BaseHierarchicalChart:
    def __init__(self, data):
        self.data = data

    def validate_data(self):
        pass

    def render(self):
        raise NotImplementedError("The render implemented in the subclass.")
