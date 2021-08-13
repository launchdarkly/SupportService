package webdriver;

import java.util.concurrent.ThreadLocalRandom;

import com.github.javafaker.Faker;

import org.openqa.selenium.By;
import org.openqa.selenium.ElementNotVisibleException;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Simulator implements Runnable {

    private static final Logger logger =
        LoggerFactory.getLogger(Simulator.class.getName());
    private Faker faker = new Faker();

    private static final int MIN = 1;
    private static final int MAX = 25;

    private int iterations;
    private String hostname;
    private String baseUrl;
    private String registerUrl;
    private String logoutUrl;
    private String releaseUrl;
    private String operationalUrl;
    private String experimentationUrl;

    public Simulator(String hostname) {
        this.hostname = hostname;
        this.baseUrl = String.format("http://%s", this.hostname);
        this.registerUrl = String.format("%s/register", this.baseUrl);
        this.logoutUrl = String.format("%s/logout", this.baseUrl);
        this.releaseUrl = String.format("%s/release", this.baseUrl);
        this.operationalUrl = String.format("%s/operational", this.baseUrl);
        this.experimentationUrl = String.format("%s/experiments", this.baseUrl);
        this.iterations = ThreadLocalRandom.current().nextInt(MIN, MAX + 1);
    }

    private boolean elementExists(WebDriver driver, String id) {
        try {
            logger.info("Looking for Element: " + id);
            driver.findElement(By.id(id));
        } catch (NoSuchElementException e) {
            logger.info("Element Not Found");
            return false;
        }
        logger.info("Element found");
        return true;
    }

    @Override
    public void run() {
        logger.info("Starting Activity for " + this.baseUrl + " with " + this.iterations + " iterations.");
        WebDriver driver = new ChromeDriver();
        try {
            for (int i = MIN; i <= this.iterations; i++) {
                Randomizer randomizer = new Randomizer();
                String email = faker.internet().emailAddress();

                driver.get(this.baseUrl);

                if (randomizer.getShouldView()) {
                    logger.info(email + " is viewing the registration page");
                    if (!elementExists(driver, "register_link")) {
                        driver.quit();
                    } else {
                        new WebDriverWait(driver, 100).until(ExpectedConditions.elementToBeClickable(By.id("register_link")));
                        WebElement registerLink = driver.findElement(By.id("register_link"));
                        registerLink.click();

                        if (randomizer.getShouldConvert()) {

                            logger.info("Registering " + email + " for " + this.baseUrl);
                            WebElement element = driver.findElement(By.name("userEmail"));
                            element.sendKeys(email);
                            element = driver.findElement(By.name("inputPassword"));
                            element.sendKeys("testing");
                            element = driver.findElement(By.name("confirmPassword"));
                            element.sendKeys("testing");
                            element.submit();

                            logger.info("Doing Random things with " + email + " for " + this.baseUrl + " " + this.iterations + " times.");

                            for (int j = MIN; j <= this.iterations; j++) {
                                driver.get(this.operationalUrl);
                                driver.get(this.releaseUrl);
                            }

                            for (int k = MIN; k <= this.iterations; k++) {
                                driver.get(this.baseUrl);
                            }

                            driver.get(this.experimentationUrl);

                            if (randomizer.getShouldView()) {
                                if (!driver.findElements(By.xpath("//*[@id=\"page-wrapper\"]/button")).isEmpty()) {
                                    logger.info("Showing NPS to " + email);
                                    driver.findElement(By.xpath("//*[@id=\"page-wrapper\"]/button")).click();
                                }
                                if (randomizer.getShouldConvert()) {
                                    logger.info("Converting NPS for " + email);
                                    if (elementExists(driver, "style_a")) {
                                        new WebDriverWait(driver, 5).until(ExpectedConditions.visibilityOfElementLocated(By.id("style_a")));
                                        new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(By.id("style_a")));
                                        WebElement styleAButton = driver.findElement(By.id("style_a"));
                                        logger.info("Converting Style A for " + email);
                                        styleAButton.click();
                                    }
                                    if (elementExists(driver, "nextButton")) {
                                        while (elementExists(driver, "nextButton")) {
                                            try {
                                                logger.info("Clicking Next");
                                                new WebDriverWait(driver, 5).until(ExpectedConditions.visibilityOfElementLocated(By.id("nextButton")));
                                                new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(By.id("nextButton")));
                                                WebElement nextButton = driver.findElement(By.id("nextButton"));
                                                nextButton.click();
                                            } catch (Exception e) {
                                                logger.info("Reached Last Button.");
                                                break;
                                            }
                                        }
                                        logger.info("Converting Style B for " + email);
                                        new WebDriverWait(driver, 5).until(ExpectedConditions.visibilityOfElementLocated(By.id("style_b")));
                                        new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(By.id("style_b")));
                                        WebElement styleBButton = driver.findElement(By.id("style_b"));
                                        styleBButton.click();
                                    }
                                } else {
                                    logger.info(email + " will not convert.");
                                }
                            } else {
                                logger.info(email + " will not see NPS survey.");
                            }

                            logger.info("Logging Out of " + this.baseUrl);
                            driver.get(this.logoutUrl);
                            Thread.sleep(1000);
                        } else {
                            logger.info(email + " will not complete registration");
                        }
                    }

                } else {
                    logger.info(email + " will not register at all.");
                }
            }

            driver.quit();
        } catch (Exception e) {
            logger.error("Error: " + e);
        } finally {
            driver.quit();
        }

    }
}
