from unittest import TestCase, skip

from elections_lk.elections import ElectionParliamentary
from gig import Ent, EntType

from infograph import DataColor, GeoMap, GeoMapDorling, Infograph


class TestElection(TestCase):
    @skip('slow')
    def test_elections(self):
        ent_list = Ent.list_from_type(EntType.PD)

        for cls_chart in [GeoMap, GeoMapDorling][-1:]:
            infograph = Infograph(
                'Sri Lankan Parliamentary Elections',
                'Final Results',
                'By Polling Division (1989 to 2020)',
                'elections.gov.lk',
            )

            for year in ElectionParliamentary.get_years():
                election = ElectionParliamentary.load(year)
                id_to_color = {}
                for result in election.pd_results:
                    pd_id = result.region_id
                    winning_party = result.party_to_votes.winning_party
                    color = DataColor.from_party(winning_party)
                    id_to_color[pd_id] = color

                infograph.add(
                    cls_chart(str(year), ent_list, id_to_color),
                )

            infograph.write(__file__ + f'.{cls_chart.__name__}.png')
