import math
import os
from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib import rcParams
from utils import Log

from infograph.core.DEFAULT import DEFAULT
from infograph.core.Plt import Plt

log = Log('Infograph')


@dataclass
class Infograph:
    supertitle: str = "Supertitle"
    title: str = "Title"
    subtitle: str = "Subtitle"
    data_source: str = "Unknown"
    author: str = '@nuuuwan'
    children: list = None
    lang: str = 'en'

    def add(self, child):
        if not self.children:
            self.children = []
        self.children.append(child)
        return self

    def before_render(self):
        plt.close()
        rcParams['font.family'] = DEFAULT.FONT_FAMILY
        plt.axis('off')

    def after_render(self):
        pass

    def render_watermark(self):
        # watermark
        Plt.text(
            (0.5, 0.5),
            f'{self.author}',
            color=(0, 0, 0, 0.01),
            p_font_size=15,
        )

    def render_titles(self):
        top_gap, bottom_gap = 0.045, 0.03
        top, bottom = 1 - top_gap, bottom_gap

        Plt.text(
            (0.5, top), self.supertitle, p_font_size=1.25, color="#808080"
        )
        Plt.text(
            (0.5, top - top_gap), self.title, p_font_size=3, color="#c00"
        )
        Plt.text(
            (0.5, top - top_gap * 2),
            self.subtitle,
            p_font_size=1.25,
            color="#808080",
        )

        Plt.text(
            (0.5, bottom),
            ' · '.join(
                [
                    f'Data from {self.data_source}',
                    f'Visualization by {self.author}',
                ]
            ),
        )

        if self.children:
            for child in self.children:
                child.render_in_title_section()

    def render_children(self):
        n = len(self.children)
        nrows = (int)(math.sqrt(n))
        ncols = (int)(math.ceil(n / nrows))
        _, axes = plt.subplots(
            ncols=ncols, nrows=nrows, figsize=(DEFAULT.WIDTH, DEFAULT.HEIGHT)
        )
        plt.subplots_adjust(
            left=DEFAULT.PADDING_X,
            right=1 - DEFAULT.PADDING_X,
            top=1 - DEFAULT.PADDING_Y,
            bottom=DEFAULT.PADDING_Y,
        )

        for i_child, child in enumerate(self.children):
            if n == 1:
                ax = axes
            elif nrows == 1:
                ax = axes[i_child]
            else:
                i_row = i_child // ncols
                i_col = i_child % ncols
                ax = axes[i_row][i_col]
            plt.sca(ax)
            child.render()

    def render(self):
        self.before_render()
        if self.children:
            self.render_children()
        self.render_titles()
        self.render_watermark()
        self.after_render()

    def write(self, path):
        self.render()
        plt.savefig(path, dpi=DEFAULT.DPI)
        log.info(f'Wrote {path}')
        # os.startfile(path)
