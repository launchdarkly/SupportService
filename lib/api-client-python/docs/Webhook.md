# Webhook

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**Links**](Links.md) |  | [optional] 
**id** | [**Id**](Id.md) |  | [optional] 
**url** | **str** | The URL of the remote webhook. | [optional] 
**secret** | **str** | If defined, the webhooks post request will include a X-LD-Signature header whose value will contain an HMAC SHA256 hex digest of the webhook payload, using the secret as the key. | [optional] 
**on** | **bool** | Whether this webhook is enabled or not. | [optional] 
**name** | **str** | The name of the webhook. | [optional] 
**tags** | **list[str]** | Tags assigned to this webhook. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


