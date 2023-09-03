import random

from utils import Log

log = Log('DataColor')
random.seed(0)


def flip_idx(color_to_key_list):
    key_to_color = {}
    for color, key_list in color_to_key_list.items():
        for key in key_list:
            if key in key_to_color:
                raise Exception(
                    f'Key "{key}" already has a color "{key_to_color[key]}".'
                )
            key_to_color[key] = color
    return key_to_color


LABEL_TO_COLOR = flip_idx(
    {
        'maroon': [
            'Western',
            'North Western',
            'North Central',
            'Central',
            'Sabaragamuwa',
            'Uva',
            'Southern',
        ],
        'orange': ['Eastern', 'Northern'],
    }
)

PARTY_TO_COLOR = flip_idx(
    {
        'green': ['UNP', 'SJB'],
        'blue': ['SLFP', 'UPFA', 'PA'],
        'maroon': ['SLPP'],
        'red': ['JVP', 'TMVP', 'EPDP', 'DPLF'],
        'yellow': ['TNA', 'ITAK', 'TULF', 'TELO', 'ACTC'],
        'orange': ['JHU'],
        'darkgreen': ['MNA', 'SLMC', 'NC', 'NUA'],
        'white': ['IND1', 'IND2', 'INDI', 'IND 1'],
    }
)


EXPENSE_TO_COLOR = flip_idx(
    {
        '#800': [
            'Agriculture & Irrigation',
            'Energy & Water',
            'Transport & Communication',
        ],
        '#f80': [
            'Civil Administration',
            'Defence',
            'Public Order & Safety',
        ],
        '#fc0': ['Interest Payments'],
        '#080': [
            'Community Services',
            'Education',
            'Health',
            'Housing',
            'Welfare',
        ],
        '#888': ['Other'],
    }
)


class DataColor:
    @staticmethod
    def from_label(label):
        return DataColor.from_key_to_color(
            LABEL_TO_COLOR,
            label,
            'gray',
        )

    @staticmethod
    def from_party(party):
        return DataColor.from_key_to_color(
            PARTY_TO_COLOR,
            party,
            'white',
        )

    @staticmethod
    def from_expense(expense):
        ALPHA = 'c'
        return (
            DataColor.from_key_to_color(
                EXPENSE_TO_COLOR,
                expense,
                '#fff',
            )
            + ALPHA
        )

    @staticmethod
    def from_key_to_color(key_to_color, key, default_color):
        if key not in key_to_color:
            log.debug(f'Could not find a color for "{key}".')
            return default_color
        return key_to_color[key]
