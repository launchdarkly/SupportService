package main.java.webdriver;

import java.util.concurrent.ThreadLocalRandom;

import com.github.javafaker.Faker;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Simulator implements Runnable {

    private static final Logger logger =
        LoggerFactory.getLogger(Simulator.class.getName());
    private Faker faker = new Faker();

    private static final int MIN = 1;
    private static final int MAX = 25;

    public int iterations;
    public String hostname;
    public String baseUrl;
    public String registerUrl;
    public String logoutUrl;
    public String releaseUrl;
    public String operationalUrl;
    public String entitlementUrl;

    public Simulator(String hostname) {
        this.hostname = hostname;
        this.baseUrl = String.format("http://%s", this.hostname);
        this.registerUrl = String.format("%s/register", this.baseUrl);
        this.logoutUrl = String.format("%s/logout", this.baseUrl);
        this.releaseUrl = String.format("%s/release", this.baseUrl);
        this.operationalUrl = String.format("%s/operational", this.baseUrl);
        this.entitlementUrl = String.format("%s/entitlement", this.baseUrl);
        this.iterations = ThreadLocalRandom.current().nextInt(MIN, MAX + 1);
    }

    @Override
    public void run() {
        logger.info("Starting Activity for " + this.baseUrl + " with " + this.iterations + " iterations.");

        try {
            WebDriver driver = new ChromeDriver();

            for (int i = MIN; i <= this.iterations; i++) {
                String email = faker.internet().emailAddress();
    
                driver.get(this.registerUrl);
    
                logger.info("Registering " + email + " for " + this.baseUrl);
                WebElement element = driver.findElement(By.name("userEmail"));
                element.sendKeys(email);
                element = driver.findElement(By.name("inputPassword"));
                element.sendKeys("testing");
                element = driver.findElement(By.name("confirmPassword"));
                element.sendKeys("testing");
                element.submit();
    
                logger.info("Logging In " + email + " for " + this.baseUrl);
                driver.get(this.baseUrl);
                element = driver.findElement(By.name("userEmail"));
                element.sendKeys(email);
                element = driver.findElement(By.name("inputPassword"));
                element.sendKeys("testing");
                element.submit();

                logger.info("Doing Random things with " + email + " for " + this.baseUrl + " " + this.iterations + " times.");

                for (int j = MIN; j <= this.iterations; j++) {
                    driver.get(this.operationalUrl);
                    driver.get(this.releaseUrl);
                }

                for (int k = MIN; k <= this.iterations; k++) {
                    driver.get(this.entitlementUrl);
                    driver.get(this.baseUrl);
                }
    
                logger.info("Logging Out of " + this.baseUrl);
                driver.get(this.logoutUrl);
                Thread.sleep(1000);
            }
    
            driver.quit();
        } catch (Exception e) {
            logger.error("Error: " + e);
        }

    }
}