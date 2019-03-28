package webdriver;

import java.util.Random;

public class Randomizer {

    private boolean shouldView;
    private boolean shouldConvert;
    private Random random = new Random();

    public Randomizer() {
        this.shouldView = random.nextBoolean();
        this.shouldConvert = random.nextBoolean();
    }

    public boolean getShouldView() {
        return this.shouldView;
    }

    public boolean getShouldConvert() {
        return this.shouldConvert;
    }
}