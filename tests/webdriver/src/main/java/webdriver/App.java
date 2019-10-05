package webdriver;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import com.launchdarkly.api.ApiClient;
import com.launchdarkly.api.Configuration;
import com.launchdarkly.api.api.ProjectsApi;
import com.launchdarkly.api.auth.ApiKeyAuth;
import com.launchdarkly.api.model.Environment;
import com.launchdarkly.api.model.Project;
import com.launchdarkly.client.LDClient;
import com.launchdarkly.client.LDUser;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Selenium Driver For SupportService
 *
 */
public class App
{
    private static final Logger logger =
        LoggerFactory.getLogger(App.class.getName());
    private static final String PROJECT_KEY = "support-service";

    public static void main( String[] args ) throws InterruptedException, IOException
    {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        ApiKeyAuth Token = (ApiKeyAuth) defaultClient.getAuthentication("Token");
        Token.setApiKey(System.getenv("LD_API_KEY"));
        ProjectsApi apiInstance = new ProjectsApi();
        LDClient ldClient = new LDClient(System.getenv("LD_CLIENT_KEY"));
        LDUser user = new LDUser("any");
        int maxThreads = ldClient.intVariation("max-selenium-threads", user, 1);
        boolean simulatorDisabled = ldClient.boolVariation("disable-simulator", user, false);

        if (simulatorDisabled) {
            logger.info("Not Running. Simualtor is disabled.");
            System.exit(0);
        }
        
        ldClient.flush();
        ldClient.close();

        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(maxThreads);

        try {
            Project result = apiInstance.getProject(PROJECT_KEY);
            List<Environment> environmentsList = result.getEnvironments();

            for (int i = 0; i < environmentsList.size(); i++) {
                String key = environmentsList.get(i).getKey();
                List<String> tag = environmentsList.get(i).getTags();
                Boolean shouldSim = true;

                String search = "nosim";
                for (String str: tag) {
                    if (str.trim().contains(search))
                    shouldSim = false;
                }

                if (shouldSim) {
                    String hostname = String.format("%s.staging.ldsolutions.org", key);
                    Simulator simulator = new Simulator(hostname);
                    executor.execute(simulator);
                } else {
                    logger.info("Found nosim tag. Not running simulator for " + key + ".");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        executor.shutdown();
    }
}
