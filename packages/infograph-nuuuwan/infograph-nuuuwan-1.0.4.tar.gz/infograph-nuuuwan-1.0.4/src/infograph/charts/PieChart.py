import matplotlib.pyplot as plt

from infograph.charts.AbstractChart import AbstractChart
from infograph.core.DataColor import DataColor
from infograph.core.DEFAULT import DEFAULT


class PieChart(AbstractChart):
    def render_custom(self):
        ax = plt.gca()
        x = self.x
        y = self.y
        colors = [DataColor.from_label(xi) for xi in x]
        ax.pie(
            y,
            labels=x,
            startangle=90,
            colors=colors,
            textprops={'fontsize': DEFAULT.FONT_SIZE_BASE},
        )
        ax.set_yticklabels(['{:,.0f}'.format(x) for x in ax.get_yticks()])
