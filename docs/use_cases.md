# Use Cases 

Run book for Feature Flagging use cases in the SupportService project 

## Operational 

### Change Logging Level Dynamically 

Debug logs provide a large amount of information to help teams figure out 
the issue when things go wrong. However, running an application in debug 
mode in production is not a viable solution because it would generate a 
massive amount of log data. Traditionally in order to change the logging 
level of an application you would change a configuration file and restart 
the application. 

With feature flags, you are able to dynamically change the logging level of 
your application without having to restart it. 

#### Create Feature Flag in LaunchDarkly 
You can try out this use case with the following steps. 

1. In LaunchDarkly, create a new multivariate feature flag called `set-logging-level` 
with the following variations: 
    * Value: 50 Name: CRITICAL
    * Value: 40 Name: ERROR
    * Value: 30 Name: WARNING
    * Value: 20 Name: INFO
    * Value: 10 Name: DEBUG
2. Under the feature flag targeting rules select "INFO" as the variation to serve 
when targeting is turned off. 
3. Turn on targeting and select the "DEBUG" variation. You should now see debug 
logs show up for all subsequent requests. 
4. Turn off targeting. You should no longer see debug logs show up for all
subsequent request.  