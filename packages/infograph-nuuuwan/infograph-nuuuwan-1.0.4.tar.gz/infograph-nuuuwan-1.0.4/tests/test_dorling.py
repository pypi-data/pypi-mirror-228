from unittest import TestCase, skip

from infograph import Bounds, Dorling, Ellipse

TEST_BOUNDS = Bounds(p1=[0, 0], p2=[4, 4])


class TestDorling(TestCase):
    @skip('SLOW')
    def test_move_to_bounds(self):
        observed_ellipse_list, did_move = Dorling.move_into_bounds(
            ellipse_list=[
                Ellipse(center=[1, 1], radii=[2, 2]),
            ],
            i_a=0,
            bounds=TEST_BOUNDS,
        )

        expected_ellipse_list = [
            Ellipse(center=[2, 2], radii=[2, 2]),
        ]
        self.assertTrue(did_move)
        self.assertEqual(observed_ellipse_list, expected_ellipse_list)

    @skip('SLOW')
    def test_get_move_delta(self):
        ellipse_a = Ellipse(center=[1, 1], radii=[2, 2])
        ellipse_b = Ellipse(center=[2, 2], radii=[2, 2])

        self.assertEqual(
            Dorling.get_move_delta(
                ellipse_list=[
                    ellipse_a,
                    ellipse_a,
                ],
                i_a=0,
                i_b=1,
            ),
            [0, 0],
        )
        self.assertEqual(
            Dorling.get_move_delta(
                ellipse_list=[
                    ellipse_a,
                    ellipse_b,
                ],
                i_a=0,
                i_b=1,
            ),
            [-0.04, -0.04],
        )

    def test_compress(self):
        self.assertEqual(
            Dorling(
                ellipse_list=[
                    Ellipse(center=[1, 1], radii=[1, 1]),
                    Ellipse(center=[2, 2], radii=[1, 1]),
                ],
                bounds=TEST_BOUNDS,
            ).compress(),
            [
                Ellipse(center=[0.995, 0.995], radii=[1, 1]),
                Ellipse(center=[3, 3], radii=[1, 1]),
            ],
        )
