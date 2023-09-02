from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ID_PROP
from cypherdataframe.garner_domain.queries.LogisticsTableQuery import \
    LogisticsTableQuery
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query

@dataclass
class AttachableTableQuery:
    attachable_label: str
    domain_label: str
    attachable_props: list[Property]
    post_label: str | None = None
    attachable_return_id: str = "a"

    def to_query(self, skip: int | None = None, limit: int | None = None):
        domain_branch = BranchMaker(
            props=[ID_PROP],
            label=self.domain_label,
            post_label=None,
            relationship=None,
            relationship_postfix=None,
            required=False,
            away_from_core=None,
            domain_label=None
        )

        table_current = LogisticsTableQuery(
            branchMakers=[domain_branch],
            label=self.attachable_label,
            post_label=None,
            return_id=self.attachable_return_id,
            props=self.attachable_props
        )
        return table_current.to_query(skip=skip, limit=limit)



