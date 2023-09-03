from dataclasses import dataclass


@dataclass
class Ellipse:
    center: list[float]
    radii: list[float]

    @property
    def center_and_radii(self):
        return [self.center, self.radii]

    def to_dict(self):
        return {
            'center': self.center,
            'radii': self.radii,
        }

    @staticmethod
    def from_dict(data):
        return Ellipse(
            center=data['center'],
            radii=data['radii'],
        )
