import matplotlib.pyplot as plt


class AbstractChart:
    def __init__(self, title, x, y):
        self.title = title
        self.x = x
        self.y = y

    def render(self):
        plt.grid(color='#f0f0f0', linestyle='-', linewidth=0.5)
        ax = plt.gca()
        plt.axis('on')
        ax.set_title(self.title)
        self.render_custom()

    def render_in_title_section(self):
        pass
