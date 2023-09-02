from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="BlockResponse")


@attr.s(auto_attribs=True)
class BlockResponse:
    """
    Attributes:
        block_number (float): Block Number. Example: 17000000.
        block_timestamp (float): The Unix timestamp of when the block was mined. Example: 1680911891.
    """

    block_number: float
    block_timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        block_response = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
        )

        return block_response
