import matplotlib.pyplot as plt
from utils import Log

from infograph.charts.AbstractChart import AbstractChart
from infograph.math.Bounds import Bounds
from infograph.math.Dorling import Dorling
from infograph.math.Ellipse import Ellipse

log = Log('GeoMap')


class GeoMapDorling(AbstractChart):
    def __init__(self, title, ent_list: list, id_to_color):
        super().__init__(title, None, None)
        self.ent_list = ent_list
        self.id_to_color = id_to_color

    def render_custom(self):
        ax = plt.gca()

        for ent in self.ent_list:
            ent.geo().plot(ax=ax, color='#f8f8f8')

        ellipse_list = []
        min_x, min_y, max_x, max_y = 180, 90, -180, -90
        for ent in self.ent_list:
            x, y = ent.lnglat
            radius = ent.population / 3_000_000
            ellipse_list.append(Ellipse([x, y], [radius, radius]))

            min_x = min(min_x, x - radius)
            min_y = min(min_y, y - radius)
            max_x = max(max_x, x + radius)
            max_y = max(max_y, y + radius)

        bounds = Bounds([min_x - 2, min_y - 2], [max_x + 2, max_y + 2])
        ellipse_list = Dorling(ellipse_list, bounds).compress()

        for i, ent in enumerate(self.ent_list):
            color = self.id_to_color[ent.id]
            x, y = ellipse_list[i].center
            radius = ellipse_list[i].radii[0]
            ax.add_patch(
                plt.Circle(
                    (x, y), radius, color=color, linewidth=0.5, alpha=0.5
                )
            )

        plt.axis('off')
