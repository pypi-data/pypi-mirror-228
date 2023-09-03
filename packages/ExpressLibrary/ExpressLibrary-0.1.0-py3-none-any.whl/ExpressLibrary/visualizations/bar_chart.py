from .base_bar_chart import BaseChart
import plotly.express as px
import plotly.graph_objects as go

class BarChart(BaseChart):
    
    def __init__(self, data, x, y):
        super().__init__(data, x, y)
        self.colors = ['blue', 'green', 'red']
        
    
    def set_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label

    def set_title(self, title):
        self.title = title

    def set_colors(self, colors):
        if not isinstance(colors, list):
            raise ValueError("Colors should be a list of color codes or names.")
        self.colors = colors
    
    def validate_data(self):
        if self.x not in self.data.columns or not all(y in self.data.columns for y in self.y):
            raise ValueError("The specified x or y columns are not in dataset.")
        
        if len(self.colors) < len(self.y):
            raise ValueError("The number of colors should be at least equal to the number of y-values")
    
    def create_layout(self):
        layout = {
            'xaxis': dict(title=self.x_label),
            'yaxis': dict(title=self.y_label),
        }
        
        if hasattr(self, 'title'):
            layout['title'] = dict(text=self.title)
        
        return layout
        
    def create_simple_bar(self):
        self.validate_data()
        traces = []    
        for i , y_val in enumerate(self.y):
            traces.append(go.Bar(x=self.data[self.x], y=self.data[y_val], name=y_val, marker_color=self.colors[i % len(self.colors)]))

        layout = self.create_layout()
        fig = go.Figure(data=traces, layout=layout)
        fig.show()
        
    def create_stacked_bar(self):
        self.validate_data()
        fig = px.bar(self.data, x=self.x, y=self.y,
                     labels={'x': self.x_label, 'y': self.y_label},
                     color_discrete_sequence=self.colors)
        
        if hasattr(self, 'title'):
            fig.update_layout(title_text=self.title)

        fig.update_layout(barmode='stack')
        fig.show()
        
    def create_grouped_bar(self):
        fig = px.bar(self.data, x=self.x, y=self.y,
                     labels= {'x': self.x_label, 'y': self.y_label},
                     color_discrete_sequence=self.colors)
        
        if hasattr(self, 'title'):
            fig.update_layout(title_text=self.title)
            
        fig.update_layout(barmode='group')
        fig.show()
