package webdriver;

import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import com.launchdarkly.api.*;
import com.launchdarkly.api.auth.*;
import com.launchdarkly.api.api.ProjectsApi;
import com.launchdarkly.api.model.Project;
import com.launchdarkly.api.model.Environment;
import com.launchdarkly.api.Configuration;
import com.launchdarkly.client.*;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import webdriver.Simulator;

/**
 * Selenium Driver For SupportService
 *
 */
public class App
{
    private static final Logger logger =
        LoggerFactory.getLogger(App.class.getName());
    private static final String PROJECT_KEY = "support-service";

    public static void main( String[] args ) throws InterruptedException
    {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        ApiKeyAuth Token = (ApiKeyAuth) defaultClient.getAuthentication("Token");
        Token.setApiKey(System.getenv("LD_API_KEY"));
        ProjectsApi apiInstance = new ProjectsApi();
        LDClient ldClient = new LDClient(System.getenv("LD_CLIENT_KEY"));
        LDUser user = new LDUser("any");
        int maxThreads = ldClient.intVariation("max-selenium-threads", user, 1);

        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(maxThreads);

        try {
            Project result = apiInstance.getProject(PROJECT_KEY);
            List<Environment> environmentsList = result.getEnvironments();

            for (int i = 0; i < environmentsList.size(); i++) {
                String key = environmentsList.get(i).getKey();
                String hostname = String.format("%s.ldsolutions.org", key);
                Simulator simulator = new Simulator(hostname);
                executor.execute(simulator);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        executor.shutdown();
    }
}
