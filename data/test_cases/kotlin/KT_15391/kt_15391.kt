class C : suspend () -> Unit {

}

fun main(args: Array<String>) {
    C().startCoroutine(completion = object : Continuation<Unit> {
        override fun resume(value: Unit) {
            TODO("not implemented")
        }

        override fun resumeWithException(exception: Throwable) {
            TODO("not implemented")
        }
    })
}
