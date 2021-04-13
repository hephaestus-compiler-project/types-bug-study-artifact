public class TestSwitchBug {
    Object func(final String name) {
    return switch (name) {
    default -> name != null && name == name;
    };
    }
    }