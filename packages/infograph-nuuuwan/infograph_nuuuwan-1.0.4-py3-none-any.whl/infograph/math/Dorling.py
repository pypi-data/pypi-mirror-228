import json
import os
import tempfile

from utils import JSONFile, Log, hashx

from infograph.math.Bounds import Bounds
from infograph.math.Ellipse import Ellipse

log = Log('Dorling')


class Dorling:
    R_PADDING = 0.0001
    D_T = 0.01
    MAX_EPOCHS = 1_000

    def __init__(self, ellipse_list: list[Ellipse], bounds: Bounds):
        self.ellipse_list = ellipse_list
        self.bounds = bounds

    def cache_key(self):
        data = dict(
            ellipse_list=[e.to_dict() for e in self.ellipse_list],
            bounds=self.bounds.to_dict(),
        )
        return hashx.md5(json.dumps(data))

    def file(self):
        return JSONFile(
            os.path.join(
                tempfile.gettempdir(), f'dorling.{self.cache_key()}.json'
            )
        )

    @staticmethod
    def move_into_bounds(ellipse_list, i_a, bounds):
        [cx_a, cy_a], [rx_a, ry_a] = ellipse_list[i_a].center_and_radii
        [minx, miny, maxx, maxy] = bounds.values

        did_move = False
        if (cx_a - rx_a) < minx:
            cx_a = minx + rx_a
            did_move = True
        elif maxx < (cx_a + rx_a):
            cx_a = maxx - rx_a
            did_move = True

        if (cy_a - ry_a) < miny:
            cy_a = miny + ry_a
            did_move = True
        elif maxy < (cy_a + ry_a):
            cy_a = maxy - ry_a
            did_move = True

        ellipse_list[i_a].center = [cx_a, cy_a]
        return ellipse_list, did_move

    @staticmethod
    def get_move_delta(ellipse_list, i_a, i_b):
        if i_a == i_b:
            return 0, 0
        [cx_a, cy_a], [rx_a, ry_a] = ellipse_list[i_a].center_and_radii
        [cx_b, cy_b], [rx_b, ry_b] = ellipse_list[i_b].center_and_radii

        dx, dy = cx_b - cx_a, cy_b - cy_a

        if (abs(dx) > (rx_a + rx_b) * (1 + Dorling.R_PADDING)) or (
            abs(dy) > (ry_a + ry_b) * (1 + Dorling.R_PADDING)
        ):
            return [0, 0]

        rb2 = ry_a**2 + ry_b**2
        d2 = dx**2 + dy**2

        if d2 == 0:
            raise Exception(f'Points {i_a} and {i_b} are overlapping.')

        f_b_a = -Dorling.D_T * (rb2) / d2
        return [dx * f_b_a, dy * f_b_a]

    def run_epoch(self, ellipse_list):
        n_ellipse_list = len(self.ellipse_list)
        n_moves = 0
        for i_a in range(0, n_ellipse_list):
            ellipse_list, did_move = Dorling.move_into_bounds(
                ellipse_list, i_a, self.bounds
            )
            if did_move:
                n_moves += 1
                continue

            sx, sy = 0, 0
            for i_b in range(0, n_ellipse_list):
                dsx, dsy = Dorling.get_move_delta(ellipse_list, i_a, i_b)

                sx += dsx
                sy += dsy

            if sx or sy:
                ellipse_list[i_a].center[0] += sx
                ellipse_list[i_a].center[1] += sy
                n_moves += 1
        return ellipse_list, n_moves

    def compress_nocache(self) -> list[Ellipse]:
        for i_epochs in range(0, Dorling.MAX_EPOCHS):
            ellipse_list, n_moves = self.run_epoch(self.ellipse_list)

            if i_epochs % (Dorling.MAX_EPOCHS / 10) == 0:
                log.debug(f'{i_epochs=} {n_moves=}')

            if n_moves == 0:
                log.debug(f'i_epochs = {i_epochs:,} - Complete')
                break
        return ellipse_list

    def compress(self) -> list[Ellipse]:
        file = self.file()
        if file.exists:
            ellipse_list = [Ellipse.from_dict(d) for d in file.read()]
        else:
            ellipse_list = self.compress_nocache()
            file.write([e.to_dict() for e in ellipse_list])
        return ellipse_list
