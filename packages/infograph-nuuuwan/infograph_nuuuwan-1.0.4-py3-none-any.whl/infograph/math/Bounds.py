from dataclasses import dataclass


@dataclass
class Bounds:
    p1: list[float]
    p2: list[float]

    @property
    def values(self):
        return [*self.p1, *self.p2]

    def to_dict(self):
        return {
            'p1': self.p1,
            'p2': self.p2,
        }
