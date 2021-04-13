class Foo {
    suspend operator fun <T> invoke(body: suspend (Int) -> T) = null as T
    suspend fun <T> bar(body: suspend (Int) -> T) = null as T
}

fun <T> runBlocking(block: suspend () -> T) = null as T

fun main() {
    val retry = Foo()
    runBlocking {
        retry { 1 } // NI: "Suspend function 'invoke' should be called only from a coroutine or another suspend function", OI – OK
    }
    runBlocking {
        retry { 1 } // OK
        1
    }
    runBlocking {
        retry.bar { 1 } // OK
    }
}
