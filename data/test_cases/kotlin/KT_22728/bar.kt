package bar

import foo.*

fun foo(f: MyHandler<Int>) {}

fun test() {
    foo {
        this
    }
}
