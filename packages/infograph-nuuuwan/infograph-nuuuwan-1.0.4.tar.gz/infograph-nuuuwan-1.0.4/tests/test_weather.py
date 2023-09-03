from unittest import TestCase

from infograph import BarChart, DataTable, Infograph, RangeBarChart

TEST_WEATHER_DATA_PATH = 'tests/weather.tsv'
TEST_WEATHER_DATA_TABLE = DataTable.from_file(TEST_WEATHER_DATA_PATH)


class TestWeather(TestCase):
    def get_temp_chart(self):
        a = 0.7

        def func_color(_, __, y2i):
            for limit, color in [
                [35, (0.5, 0, 0, a)],
                [30, (1, 0, 0, a)],
                [25, (1, 0.5, 0, a)],
                [20, (0, 1, 0, a)],
                [15, (0, 0.5, 1, a)],
                [10, (0, 0, 1, a)],
            ]:
                if y2i > limit:
                    return color
            return (0, 0, 0.5, a)

        TEST_WEATHER_DATA_TABLE.sort('max_temp_c', reverse=False)
        return RangeBarChart(
            'Temperature (°C)',
            TEST_WEATHER_DATA_TABLE['location'],
            TEST_WEATHER_DATA_TABLE['min_temp_c'],
            TEST_WEATHER_DATA_TABLE['max_temp_c'],
            func_color,
        )

    def get_rain_chart(self):
        def func_color(_, yi):
            b = 1

            for limit, x in [
                [200, 1],
                [100, 2],
                [50, 3],
                [25, 4],
                [-1, 5],
            ]:
                if yi > limit:
                    a = 1 / x
                    g = 1 - 1 / x
                    break

            r = g / 2
            return (r, g, b, a)

        TEST_WEATHER_DATA_TABLE.sort('rain_mm', reverse=False)
        return BarChart(
            'Rainfall (mm)',
            TEST_WEATHER_DATA_TABLE['location'],
            TEST_WEATHER_DATA_TABLE['rain_mm'],
            func_color,
        )

    def test_all(self):
        infograph = Infograph(
            'Sri Lanka',
            'Temperature & Rainfall',
            '2023-01-23',
            'meteo.gov.lk',
        )
        infograph.add(self.get_rain_chart())
        infograph.add(self.get_temp_chart())
        infograph.write(__file__ + '.png')
