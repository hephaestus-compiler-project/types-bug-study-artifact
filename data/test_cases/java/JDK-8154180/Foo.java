import java.util.function.Consumer;
import java.nio.ByteBuffer;

class Foo {
    Foo(Consumer<ByteBuffer> cb) {
    }

    public static void main(String[] args) {
        Foo foo = new Foo((b -> System.out.println(asString(b))));
    }

    static String asString(ByteBuffer buf) {
        return null;
    }
}
