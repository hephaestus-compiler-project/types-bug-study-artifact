public class SwitchTest {
    public String convert(int i) {
        return switch (i) {
            default -> throw new AssertionError();
        };
    }
}
