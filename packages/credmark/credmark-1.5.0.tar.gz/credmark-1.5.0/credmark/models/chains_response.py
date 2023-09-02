from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.chain import Chain


T = TypeVar("T", bound="ChainsResponse")


@attr.s(auto_attribs=True)
class ChainsResponse:
    """
    Attributes:
        chains (List['Chain']):
    """

    chains: List["Chain"]

    def to_dict(self) -> Dict[str, Any]:
        chains = []
        for chains_item_data in self.chains:
            chains_item = chains_item_data.to_dict()

            chains.append(chains_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chains": chains,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chain import Chain

        d = src_dict.copy()
        chains = []
        _chains = d.pop("chains")
        for chains_item_data in _chains:
            chains_item = Chain.from_dict(chains_item_data)

            chains.append(chains_item)

        chains_response = cls(
            chains=chains,
        )

        return chains_response
