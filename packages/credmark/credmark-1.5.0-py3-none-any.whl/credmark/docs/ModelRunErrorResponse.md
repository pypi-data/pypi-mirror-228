# ModelRunErrorResponse


## Properties
Name | Type | Description
------------ | ------------- | -------------
slug | str | Short identifying name for the model
version | str | Version of the model
chain_id | float | Chain id
block_number | float | Block number
block_timestamp | float | Block timestamp
dependencies | Dict[str, Any] | Dictionary of model dependencies, model name to version or version list.
cached | bool | Whether it is a cached result
runtime | float | Running time of the model in milliseconds.
error | Union[Unset, ModelRunResponseError] | 

