public interface Base {
    String getValue();

    default String test() {
        return getValue();
    }
}

