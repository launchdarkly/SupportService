package webdriver;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import org.slf4j.LoggerFactory;

import main.java.webdriver.Simulator;



/**
 * Selenium Driver For SupportService
 *
 */
public class App 
{
    private static final Logger logger =
        LoggerFactory.getLogger(App.class.getName());
    private static final int MAX_THREADS = 3;

    public static void main( String[] args ) throws IOException, InterruptedException
    {
        BufferedReader br = new BufferedReader(new FileReader("hosts.txt"));
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(MAX_THREADS);

        for (String line = br.readLine(); line != null; line = br.readLine()) {
            Simulator simulator = new Simulator(line);
            executor.execute(simulator);
        }

        executor.shutdown();
    }
}
