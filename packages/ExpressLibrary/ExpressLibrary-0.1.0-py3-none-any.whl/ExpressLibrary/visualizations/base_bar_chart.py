class BaseChart:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x if x else self.data.columns[0]
        self.y = y if y else self.data.columns[1:]
        self.colors = None
        self.x_label = None
        self.y_label = None
        self.title = None
    
    def load_data(self, data):
        self.data = data
    

    def set_axes(self, x, y):
        self.x = x
        self.y = y
    
    def set_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label
    
    def set_colors(self, colors):
        self.colors = colors
    
    def set_title(self, title):
        self.title = title

    def basic_styling(self):
        pass