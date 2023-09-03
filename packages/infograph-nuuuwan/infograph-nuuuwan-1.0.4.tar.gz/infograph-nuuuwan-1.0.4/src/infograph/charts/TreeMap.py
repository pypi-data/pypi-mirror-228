import math

import matplotlib.pyplot as plt
import squarify
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from infograph.charts.AbstractChart import AbstractChart
from infograph.core.DEFAULT import DEFAULT
from infograph.core.Plt import Plt


class TreeMap(AbstractChart):
    P_PADDING = 0.04
    ALPHA_ICON = 0.5
    SQUARIFY_DIM = 200

    def __init__(self, title, x, y, color=None):
        self.title = title
        self.x = x
        self.y = y
        self.color = color

    @property
    def icon_image_path(self):
        return 'tests/ballot.png'

    @property
    def units_per_icon(_):
        return 10

    @property
    def im(self):
        return plt.imread(self.icon_image_path)

    @property
    def icon_title(self):
        return 'Cost of the 2023 Local Government Election (LKR 10B)'

    def render_custom(self):
        ax = plt.gca()
        im = self.im
        width_im, height_im = im.shape[0], im.shape[1]
        squarify.plot(
            sizes=self.y,
            label=None,
            color=self.color,
            pad=True,
            norm_y=self.SQUARIFY_DIM,
            norm_x=(int)(DEFAULT.WIDTH * self.SQUARIFY_DIM / DEFAULT.HEIGHT),
        )

        for i_datum, rect in enumerate(ax.patches):
            left, bottom = rect.get_x(), rect.get_y()
            width_outer, height_outer = rect.get_width(), rect.get_height()

            padding_x, padding_y = (
                self.P_PADDING * width_outer,
                self.P_PADDING * height_outer,
            )

            width, height = (
                width_outer - padding_x * 2,
                height_outer - padding_y * 2,
            )
            area = width * height
            n_icons = round(self.y[i_datum] / self.units_per_icon)

            n_rows = max(1, round(math.sqrt(n_icons / area) * height))
            n_cols = max(1, math.ceil(n_icons / n_rows))

            zoom = (
                2
                * min(width / n_cols / width_im, height / n_rows / height_im)
                * 100
                / self.SQUARIFY_DIM
            )
            offset_image = OffsetImage(im, zoom=zoom, alpha=self.ALPHA_ICON)

            for i_row in range(n_rows):
                for i_col in range(n_cols):
                    i_cell = i_row * n_cols + i_col
                    if i_cell >= n_icons:
                        break

                    px = i_col / n_cols
                    py = i_row / n_rows

                    x_icon = left + width * px + padding_x
                    y_icon = bottom + height * (1 - py) + padding_y

                    box = AnnotationBbox(
                        offsetbox=offset_image,
                        xy=(
                            x_icon,
                            y_icon,
                        ),
                        box_alignment=(-0.25, 1),
                        frameon=False,
                    )
                    ax.add_artist(box)

            name = self.x[i_datum]
            label = f'{name} - {n_icons}'
            fontsize = min(
                18,
                0.4 * area / self.SQUARIFY_DIM,
                width / len(label) * 2.3,
            )
            ax.annotate(
                label,
                (
                    left + width / 2 + padding_x,
                    bottom + height / 2 + padding_y,
                ),
                fontsize=fontsize,
                horizontalalignment='center',
                verticalalignment='center',
                color="#fff",
                bbox=dict(
                    edgecolor=(0.75, 0, 0, 0.1),
                    facecolor=(0.75, 0, 0, 0.5),
                    boxstyle='round',
                ),
            )

        plt.axis('off')

    def render_in_title_section(self):
        im = self.im
        offset_image = OffsetImage(im, zoom=0.035, alpha=self.ALPHA_ICON)
        box = AnnotationBbox(
            offsetbox=offset_image,
            xy=(
                0,
                0,
            ),
            box_alignment=(-8.7, 2.4),
            frameon=False,
        )
        plt.gca().add_artist(box)
        Plt.text(
            (0.5, 0.11),
            ' = ' + self.icon_title,
            p_font_size=1.25,
            color="#808080",
        )
