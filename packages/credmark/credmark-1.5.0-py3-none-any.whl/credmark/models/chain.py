from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Chain")


@attr.s(auto_attribs=True)
class Chain:
    """
    Attributes:
        chain_id (float): Unique identifier that represents the blockchain network. Example: 1.
        name (str): Common name of the chain. Example: Mainnet.
        has_ledger (bool): If the chain has indexed data available for the models. Example: True.
        has_node (bool): If the chain has a web3 node available for the models. Example: True.
    """

    chain_id: float
    name: str
    has_ledger: bool
    has_node: bool

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        name = self.name
        has_ledger = self.has_ledger
        has_node = self.has_node

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "name": name,
                "hasLedger": has_ledger,
                "hasNode": has_node,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain_id = d.pop("chainId")

        name = d.pop("name")

        has_ledger = d.pop("hasLedger")

        has_node = d.pop("hasNode")

        chain = cls(
            chain_id=chain_id,
            name=name,
            has_ledger=has_ledger,
            has_node=has_node,
        )

        return chain
