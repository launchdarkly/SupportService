# launchdarkly_api.AuditLogApi

All URIs are relative to *https://app.launchdarkly.com/api/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_audit_log_entries**](AuditLogApi.md#get_audit_log_entries) | **GET** /auditlog | Get a list of all audit log entries. The query parameters allow you to restrict the returned results by date ranges, resource specifiers, or a full-text search query.
[**get_audit_log_entry**](AuditLogApi.md#get_audit_log_entry) | **GET** /auditlog/{resourceId} | Use this endpoint to fetch a single audit log entry by its resouce ID.


# **get_audit_log_entries**
> AuditLogEntries get_audit_log_entries(before=before, after=after, q=q, limit=limit, spec=spec)

Get a list of all audit log entries. The query parameters allow you to restrict the returned results by date ranges, resource specifiers, or a full-text search query.

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
api_instance = launchdarkly_api.AuditLogApi(launchdarkly_api.ApiClient(configuration))
before = 8.14 # float | A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries returned will have before this timestamp. (optional)
after = 8.14 # float | A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries returned will have occured after this timestamp. (optional)
q = 'q_example' # str | Text to search for. You can search for the full or partial name of the resource involved or fullpartial email address of the member who made the change. (optional)
limit = 8.14 # float | A limit on the number of audit log entries to be returned, between 1 and 20. (optional)
spec = 'spec_example' # str | A resource specifier, allowing you to filter audit log listings by resource. (optional)

try:
    # Get a list of all audit log entries. The query parameters allow you to restrict the returned results by date ranges, resource specifiers, or a full-text search query.
    api_response = api_instance.get_audit_log_entries(before=before, after=after, q=q, limit=limit, spec=spec)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditLogApi->get_audit_log_entries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **before** | **float**| A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries returned will have before this timestamp. | [optional] 
 **after** | **float**| A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries returned will have occured after this timestamp. | [optional] 
 **q** | **str**| Text to search for. You can search for the full or partial name of the resource involved or fullpartial email address of the member who made the change. | [optional] 
 **limit** | **float**| A limit on the number of audit log entries to be returned, between 1 and 20. | [optional] 
 **spec** | **str**| A resource specifier, allowing you to filter audit log listings by resource. | [optional] 

### Return type

[**AuditLogEntries**](AuditLogEntries.md)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_audit_log_entry**
> AuditLogEntry get_audit_log_entry(resource_id)

Use this endpoint to fetch a single audit log entry by its resouce ID.

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
api_instance = launchdarkly_api.AuditLogApi(launchdarkly_api.ApiClient(configuration))
resource_id = 'resource_id_example' # str | The resource ID.

try:
    # Use this endpoint to fetch a single audit log entry by its resouce ID.
    api_response = api_instance.get_audit_log_entry(resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditLogApi->get_audit_log_entry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| The resource ID. | 

### Return type

[**AuditLogEntry**](AuditLogEntry.md)

### Authorization

[Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

