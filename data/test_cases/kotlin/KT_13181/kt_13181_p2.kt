//module B
import org.junit.Test

class FooTest {

    @Test
    fun baz() {
        val b: Foo<String>.Bar = {}
        Foo("").baz(b)
    }

}
