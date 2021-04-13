public class Test {

    public static void t() {
        Exception ex = null;
        error("error", ex); //ambiguous error here
    }

    public static void error(Object object, Object... params) {
    }

    public static void error(Object object, Throwable t, Object... params) {
    }
}
