import plotly.express as px
from .base_heatmap import BaseHeatmapChart

class HeatmapChart(BaseHeatmapChart):
    def __init__(self,data, title="", color_scheme="Viridis"):
        super().__init__(title=title)
        self.data = data
        self.color_scheme = color_scheme
    

    def set_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme
    
    def render(self):

        fig = px.imshow(self.data, labels=dict(x="X Axis", y="Y Axis", color="Value"),
                        title=self.title, 
                        color_continuous_scale=self.color_scheme)
        fig.show()



