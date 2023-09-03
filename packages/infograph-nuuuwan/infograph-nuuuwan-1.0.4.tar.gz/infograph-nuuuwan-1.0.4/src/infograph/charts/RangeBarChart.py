import matplotlib.pyplot as plt

from infograph.charts.BarChart import BarChart


class RangeBarChart(BarChart):
    def __init__(self, title, x, y, y2, func_color):
        self.title = title
        self.x = x
        self.y = y
        self.y2 = y2
        self.func_color = func_color

    @property
    def colors(self):
        if self.func_color:
            return [
                self.func_color(xi, yi, y2i)
                for xi, yi, y2i in zip(self.x, self.y, self.y2)
            ]
        else:
            return None

    @property
    def dy(self):
        return [max(y2i - yi, 0.1) for yi, y2i in zip(self.y, self.y2)]

    def render_custom_inner(self):
        ax = plt.gca()
        x = self.x
        y = self.y
        dy = self.dy

        y_min = min(self.y)
        y_max = max(self.y2)
        padding = (y_max - y_min) * 0.1
        plt.ylim([y_min - padding, y_max + padding])

        ax.bar(x, y, color="white")
        ax.bar(x, dy, bottom=y, color=self.colors)
