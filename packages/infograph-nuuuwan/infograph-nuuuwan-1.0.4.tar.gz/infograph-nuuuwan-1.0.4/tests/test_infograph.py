from unittest import TestCase

from gig import Ent, EntType

from infograph import BarChart, DataTable, Infograph, PieChart


def get_test_infograph():
    return Infograph(
        supertitle='Sri Lanka',
        title='Population',
        subtitle='By Province (2012)',
        data_source='statistics.gov.lk',
    )


def get_province_data_table():
    return DataTable(
        [
            dict(name=ent.name, population=ent.population)
            for ent in Ent.list_from_type(EntType.PROVINCE)
        ]
    )


CHART_LIST = [BarChart, PieChart]


class TestInfograph(TestCase):
    def test_init(self):
        infograph = Infograph()
        self.assertIsNotNone(infograph)

        infograph.write(__file__ + '.png')

    def test_charts(self):
        data_table = get_province_data_table()

        for cls_chart in CHART_LIST:
            infograph = get_test_infograph()
            infograph.add(
                cls_chart(
                    'Test', data_table['name'], data_table['population']
                )
            )
            infograph.write(__file__ + f'.{cls_chart.__name__}.png')

    def test_children(self):
        data_table = get_province_data_table()
        infograph = get_test_infograph()

        for cls_chart in CHART_LIST:
            infograph.add(
                cls_chart(
                    'Test', data_table['name'], data_table['population']
                )
            )
        infograph.write(__file__ + '.children.png')
