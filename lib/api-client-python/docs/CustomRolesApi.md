# launchdarkly_api.CustomRolesApi

All URIs are relative to *https://app.launchdarkly.com/api/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_custom_role**](CustomRolesApi.md#delete_custom_role) | **DELETE** /roles/{customRoleKey} | Delete a custom role by key.
[**get_custom_role**](CustomRolesApi.md#get_custom_role) | **GET** /roles/{customRoleKey} | Get one custom role by key.
[**get_custom_roles**](CustomRolesApi.md#get_custom_roles) | **GET** /roles | Return a complete list of custom roles.
[**patch_custom_role**](CustomRolesApi.md#patch_custom_role) | **PATCH** /roles/{customRoleKey} | Modify a custom role by key.
[**post_custom_role**](CustomRolesApi.md#post_custom_role) | **POST** /roles | Create a new custom role.


# **delete_custom_role**
> delete_custom_role(custom_role_key)

Delete a custom role by key.

### Example
```python
from __future__ import print_function
import time
import launchdarkly_api
from launchdarkly_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: Token
configuration = launchdarkly_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = launchdarkly_api.CustomRolesApi(launchdarkly_api.ApiClient(configuration))
custom_role_key = 'custom_role_key_example' # str | The custom role key.

try:
    # Delete a custom role by key.
    api_instance.delete_custom_role(custom_role_key)
except ApiException as e:
    print("Exception when calling CustomRolesApi->delete_custom_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_role_key** | **str**| The custom role key. | 

### Return type

void (empty response body)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_role**
> CustomRole get_custom_role(custom_role_key)

Get one custom role by key.

### Example
```python
from __future__ import print_function
import time
import launchdarkly_api
from launchdarkly_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: Token
configuration = launchdarkly_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = launchdarkly_api.CustomRolesApi(launchdarkly_api.ApiClient(configuration))
custom_role_key = 'custom_role_key_example' # str | The custom role key.

try:
    # Get one custom role by key.
    api_response = api_instance.get_custom_role(custom_role_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomRolesApi->get_custom_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_role_key** | **str**| The custom role key. | 

### Return type

[**CustomRole**](CustomRole.md)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_roles**
> CustomRoles get_custom_roles()

Return a complete list of custom roles.

### Example
```python
from __future__ import print_function
import time
import launchdarkly_api
from launchdarkly_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: Token
configuration = launchdarkly_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = launchdarkly_api.CustomRolesApi(launchdarkly_api.ApiClient(configuration))

try:
    # Return a complete list of custom roles.
    api_response = api_instance.get_custom_roles()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomRolesApi->get_custom_roles: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CustomRoles**](CustomRoles.md)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_custom_role**
> CustomRole patch_custom_role(custom_role_key, patch_delta)

Modify a custom role by key.

### Example
```python
from __future__ import print_function
import time
import launchdarkly_api
from launchdarkly_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: Token
configuration = launchdarkly_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = launchdarkly_api.CustomRolesApi(launchdarkly_api.ApiClient(configuration))
custom_role_key = 'custom_role_key_example' # str | The custom role key.
patch_delta = [launchdarkly_api.PatchOperation()] # list[PatchOperation] | Requires a JSON Patch representation of the desired changes to the project. 'http://jsonpatch.com/'

try:
    # Modify a custom role by key.
    api_response = api_instance.patch_custom_role(custom_role_key, patch_delta)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomRolesApi->patch_custom_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_role_key** | **str**| The custom role key. | 
 **patch_delta** | [**list[PatchOperation]**](PatchOperation.md)| Requires a JSON Patch representation of the desired changes to the project. &#39;http://jsonpatch.com/&#39; | 

### Return type

[**CustomRole**](CustomRole.md)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_custom_role**
> post_custom_role(custom_role_body)

Create a new custom role.

### Example
```python
from __future__ import print_function
import time
import launchdarkly_api
from launchdarkly_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: Token
configuration = launchdarkly_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = launchdarkly_api.CustomRolesApi(launchdarkly_api.ApiClient(configuration))
custom_role_body = launchdarkly_api.CustomRoleBody() # CustomRoleBody | New role or roles to create.

try:
    # Create a new custom role.
    api_instance.post_custom_role(custom_role_body)
except ApiException as e:
    print("Exception when calling CustomRolesApi->post_custom_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_role_body** | [**CustomRoleBody**](CustomRoleBody.md)| New role or roles to create. | 

### Return type

void (empty response body)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

