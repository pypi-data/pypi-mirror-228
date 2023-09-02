# Utilities API


Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_chains**](#get_chains) | GET /v1/utilities/chains | Returns metadata for the list of blockchains supported by Credmark platform.
[**get_latest_block**](#get_latest_block) | GET /v1/utilities/chains/{chainId}/block/latest | Returns latest block of the specified chain.
[**block_to_timestamp**](#block_to_timestamp) | GET /v1/utilities/chains/{chainId}/block/to-timestamp | Returns block timestamp of the specified block number.
[**block_from_timestamp**](#block_from_timestamp) | GET /v1/utilities/chains/{chainId}/block/from-timestamp | Returns block on or before the specified block timestamp.
[**cross_chain_block**](#cross_chain_block) | GET /v1/utilities/chains/{chainId}/block/cross-chain | Returns cross chain's block on or before the timestamp of input chain's block number.


# **get_chains**

Get list of chains.

 Returns metadata for the list of blockchains supported by Credmark platform.



### Response Type
ChainsResponse

# **get_latest_block**

Get latest block.

 Returns latest block of the specified chain.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain


### Response Type
BlockResponse

# **block_to_timestamp**

Convert block number to timestamp.

 Returns block timestamp of the specified block number.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
block_number | float | Block number.


### Response Type
BlockResponse

# **block_from_timestamp**

Get block number from timestamp.

 Returns block on or before the specified block timestamp.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
timestamp | float | Unix timestamp - finds a block at or before the number of seconds since January 1, 1970.


### Response Type
BlockResponse

# **cross_chain_block**

Get equivalent cross-chain block.

 Returns cross chain's block on or before the timestamp of input chain's block number.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
block_number | float | Block number.
cross_chain_id | int | Cross chain ID


### Response Type
BlockResponse

