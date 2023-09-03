import circlify
import matplotlib.pyplot as plt
from .base_packing_chart import BasePackingChart


class SimpleCirclePackingChart(BasePackingChart):
    def render(self):
        self.validate_data()
        circles = circlify.circlify(
            self.data,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )
        
        fig, ax = plt.subplots()
        ax.set_title(self.title if self.title else 'Basic Circle Packing Chart')
        ax.axis('off')
        # ax.set_aspect('equal', 'box')
        
        for circle in circles:
            x, y, r = circle
            ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2))
        
        plt.show()


class HierarchicalCirclePackingChart(BasePackingChart):
    def render(self):
        self.validate_data()
        
        circles = circlify.circlify(
            self.data,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )
        
        fig, ax = plt.subplots(figsize=(14, 14))
        ax.set_title(self.title if self.title else 'Hierarchical Circle Packing Chart')
        ax.axis('off')
        
        # Find axis boundaries
        lim = max(
            max(
                abs(circle.x) + circle.r,
                abs(circle.y) + circle.r,
            )
            for circle in circles
        )
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)
        
        for circle in circles:
            if circle.level != 2:
                continue
            x, y, r = circle
            ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=2, color="lightblue"))
        
        for circle in circles:
            if circle.level != 3:
                continue
            x, y, r = circle
            label = circle.ex["id"]
            ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=2, color="#69b3a2"))
            plt.annotate(label, (x, y), ha='center', color="white")
        
        for circle in circles:
            if circle.level != 2:
                continue
            x, y, r = circle
            label = circle.ex["id"]
            plt.annotate(label, (x, y), va='center', ha='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.5))        
        plt.show()