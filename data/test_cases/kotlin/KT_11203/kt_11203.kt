object A

operator fun A.get(index: Int): Int = index
operator fun A.set(index: Int, newValue: String) {}

fun main(args: Array<String>) {
    val x: Int = A[0]++
}
