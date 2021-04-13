fun foo(x: Int): Either<String, Int> =
    if (x == 0) {
        x.right()
    } else {
        bar()
    }

fun bar(): Either<String, Nothing> = "".left()

fun <A> A.left(): Either<A, Nothing> = Either.Left(this)

fun <A> A.right(): Either<Nothing, A> = Either.Right(this)

open class Either<out A, out B> {
    data class Left<out A>(val a: A) : Either<A, Nothing>() {
        companion object {
            operator fun <A> invoke(a: A): Either<A, Nothing> = Left(a)
        }
    }

    data class Right<out B>(val b: B) : Either<Nothing, B>() {
        companion object {
            operator fun <B> invoke(b: B): Either<Nothing, B> = Right(b)
        }
    }
}

