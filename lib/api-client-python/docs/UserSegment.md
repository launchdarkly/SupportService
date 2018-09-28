# UserSegment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Unique identifier for the user segment. | 
**name** | **str** | Name of the user segment. | 
**description** | **str** | Description of the user segment. | [optional] 
**tags** | **list[str]** | An array of tags for this user segment. | [optional] 
**creation_date** | **float** | A unix epoch time in milliseconds specifying the creation time of this flag. | 
**included** | **list[str]** | An array of user keys that are included in this segment. | [optional] 
**excluded** | **list[str]** | An array of user keys that should not be included in this segment, unless they are also listed in \&quot;included\&quot;. | [optional] 
**rules** | [**list[UserSegmentRule]**](UserSegmentRule.md) | An array of rules that can cause a user to be included in this segment. | [optional] 
**version** | **int** |  | [optional] 
**links** | [**Links**](Links.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


