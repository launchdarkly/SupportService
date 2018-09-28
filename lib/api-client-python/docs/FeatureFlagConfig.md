# FeatureFlagConfig

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**on** | **bool** |  | [optional] 
**archived** | **bool** |  | [optional] 
**salt** | **str** |  | [optional] 
**sel** | **str** |  | [optional] 
**last_modified** | **int** |  | [optional] 
**version** | **int** |  | [optional] 
**targets** | [**list[Target]**](Target.md) |  | [optional] 
**goal_ids** | **list[str]** |  | [optional] 
**rules** | [**list[Rule]**](Rule.md) |  | [optional] 
**fallthrough** | [**Fallthrough**](Fallthrough.md) |  | [optional] 
**off_variation** | **int** |  | [optional] 
**prerequisites** | [**list[Prerequisite]**](Prerequisite.md) |  | [optional] 
**track_events** | **bool** | Set to true to send detailed event information for this flag. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


