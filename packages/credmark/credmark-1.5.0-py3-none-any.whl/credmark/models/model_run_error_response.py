from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_run_response_error import ModelRunResponseError


T = TypeVar("T", bound="ModelRunErrorResponse")


@attr.s(auto_attribs=True)
class ModelRunErrorResponse:
    """
    Attributes:
        slug (str): Short identifying name for the model Example: var.
        version (str): Version of the model Example: 1.0.
        chain_id (float): Chain id
        block_number (float): Block number
        block_timestamp (float): Block timestamp
        dependencies (Dict[str, Any]): Dictionary of model dependencies, model name to version or version list. Example:
            {"x": "1.0", "y": ["2.0", "2.1"]}.
        cached (bool): Whether it is a cached result Example: True.
        runtime (float): Running time of the model in milliseconds. Example: 5100.
        error (Union[Unset, ModelRunResponseError]):
    """

    slug: str
    version: str
    chain_id: float
    block_number: float
    block_timestamp: float
    dependencies: Dict[str, Any]
    cached: bool
    runtime: float
    error: Union[Unset, "ModelRunResponseError"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        slug = self.slug
        version = self.version
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        dependencies = self.dependencies
        cached = self.cached
        runtime = self.runtime
        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "slug": slug,
                "version": version,
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "dependencies": dependencies,
                "cached": cached,
                "runtime": runtime,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_run_response_error import ModelRunResponseError

        d = src_dict.copy()
        slug = d.pop("slug")

        version = d.pop("version")

        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        dependencies = d.pop("dependencies")

        cached = d.pop("cached")

        runtime = d.pop("runtime")

        _error = d.pop("error", UNSET)
        error: Union[Unset, ModelRunResponseError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = ModelRunResponseError.from_dict(_error)

        model_run_error_response = cls(
            slug=slug,
            version=version,
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            dependencies=dependencies,
            cached=cached,
            runtime=runtime,
            error=error,
        )

        return model_run_error_response
