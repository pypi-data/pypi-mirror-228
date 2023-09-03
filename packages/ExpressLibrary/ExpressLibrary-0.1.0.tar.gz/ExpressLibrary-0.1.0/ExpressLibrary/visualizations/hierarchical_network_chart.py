from .base_hierarchical_chart import BaseHierarchicalChart
import plotly.express as px


class HierarchicalNetworkChart(BaseHierarchicalChart):
    def set_hierarchy(self, hierarchy):
        self.hierarchy = hierarchy

    def render(self):
        # Validate data first
        self.validate_data()
        
        # Generate chart
        fig = px.sunburst(
            self.hierarchy,
            path=['Parent', 'Name'],  # Use the columns in the path argument
            title='Hierarchical Network Chart',
        )
        fig.show()