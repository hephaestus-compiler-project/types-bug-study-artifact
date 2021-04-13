fun foo(): Any? {
    return if (true) {
        if (true) {
            Bar.bar()
        } else {
            1
        }
    } else {
        1
    }
}
