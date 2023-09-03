from .base_bar_chart import BaseChart
import plotly.graph_objects as go

class ScatterPlot(BaseChart):
    def __init__(self, data, x,y, dot_size=6):
        super().__init__(data, x,y)
        self.dot_size = dot_size

    def set_dot_size(self, dot_size):
        self.dot_size = dot_size
    
    def set_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label

    def set_colors(self, colors):
        self.colors = colors
    
    def set_hover_text(self, hover_text_column):
        self.hover_text = self.data[hover_text_column]
    
    def set_varying_dot_sizes(self, size_column):
        self.varying_dot_sizes = self.data[size_column]

        
    def render(self):
        hover_text = self.hover_text if hasattr(self, 'hover_text') else None
        varying_dot_sizes = self.varying_dot_sizes if hasattr(self, 'varying_dot_sizes') else self.dot_size
        fig = go.Figure(data=[go.Scatter(x=self.data[self.x], y=self.data[self.y], mode='markers',
                                         marker=dict(size=varying_dot_sizes, 
                                                     color=self.colors),
                                                     text=hover_text
        )])
        fig.update_xaxes(title_text=self.x_label)
        fig.update_yaxes(title_text=self.y_label)
        fig.show()