annotation class Ann
open class My
fun foo() {
    val v = @Ann object: My() {}
}
