from unittest import TestCase

from infograph import Infograph, TreeMap
from infograph.core.DataColor import DataColor

GOSL_EXPENSE_DATA = {
    'Agriculture & Irrigation': 147.669,
    'Energy & Water': 97.905,
    'Transport & Communication': 310.297,
    'Civil Administration': 189.554,
    'Defence': 257.918,
    'Public Order & Safety': 113.833,
    'Interest Payments': 1048.382,
    # 'Community Services': 51.144,
    'Education': 310.613,
    'Health': 387.121,
    # 'Housing': 18.333,
    'Welfare': 397.343,
    'Other': 207.036,
}

SOE_LOSS_DATA = {
    'CPC in 2020': -2,
    'CPC in 2021': 82,
    'CPC in 2022 (Jan to Apr)': 628,
    'Sri Lankan Airlines in 2020': 45,
    'Sri Lankan Airlines in 2021': 171,
    'Sri Lankan Airlines in 2022 (Jan to Apr)': 248,
    'CEB in 2020': 60,
    'CEB in 2021': 21,
    'CEB in 2022 (Jan to Apr)': 47,
}


LANG = 'en'


class TestTreeMap(TestCase):
    def test_gosl_expense(self):
        infograph = Infograph(
            'Government of Sri Lanka',
            'Annual Expenditure',
            '2021',
            'the Annual Report (2021) of the Central Bank of Sri Lanka',
            lang=LANG,
        )

        x = list(GOSL_EXPENSE_DATA.keys())
        y = list(GOSL_EXPENSE_DATA.values())
        color = ["#fff" for expense in x]

        treemap = TreeMap('', x, y, color)
        infograph.add(treemap)
        infograph.write(__file__ + f'.gosl_expense.{LANG}.png')

    def test_seo_losses(self):
        infograph = Infograph(
            ' · '.join(
                [
                    'Ceylon Petroleum Corporation',
                    'Sri Lankan Airlines',
                    'Ceylon Electricity Board',
                ]
            ),
            'Losses',
            '2020 to 2022 Apr',
            'publicfinance.lk',
            lang=LANG,
        )

        x = list(SOE_LOSS_DATA.keys())
        y = list(SOE_LOSS_DATA.values())
        color = [DataColor.from_expense(expense) for expense in x]

        treemap = TreeMap('', x, y, color)
        infograph.add(treemap)
        infograph.write(__file__ + f'.seo_losses.{LANG}.png')
