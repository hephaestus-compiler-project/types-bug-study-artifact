class X<T>(val t: T) {
    constructor(t:String) : this(t) {} // bogus error, should be something about cannot cast String to T
}
