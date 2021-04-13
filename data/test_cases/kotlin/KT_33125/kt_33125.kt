import kotlin.experimental.ExperimentalTypeInference
interface Foo<T>
@UseExperimental(ExperimentalTypeInference::class)
fun <T> myflow(@BuilderInference block: Foo<T>.() -> Unit): Foo<T> = TODO()
fun fail(map: MutableMap<Int, Any>): Foo<Any> {
    return myflow {
        map[0] = Any()
    }
}
