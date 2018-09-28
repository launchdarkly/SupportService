# FeatureFlagBody

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A human-friendly name for the feature flag. Remember to note if this flag is intended to be temporary or permanent. | 
**key** | **str** | A unique key that will be used to reference the flag in your code. | 
**description** | **str** | A description of the feature flag. | [optional] 
**variations** | [**list[Variation]**](Variation.md) | An array of possible variations for the flag. | 
**temporary** | **bool** | Whether or not the flag is a temporary flag. | [optional] 
**tags** | **list[str]** | Tags for the feature flag. | [optional] 
**include_in_snippet** | **bool** | Whether or not this flag should be made available to the client-side JavaScript SDK. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


