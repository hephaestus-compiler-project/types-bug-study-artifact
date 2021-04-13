public class Puke {
    public static void main(String[] args) {
        doit(/* (Long) */ null, new Exception());
    }

    public static void doit(Long l) {
    }

    public static void doit(Exception... exception) {
    }

    public static void doit(Long l, Exception... exception) {
    }
}
