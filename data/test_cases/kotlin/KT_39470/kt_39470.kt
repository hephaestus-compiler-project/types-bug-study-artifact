interface Foo

interface Bar {
    val serializationWhitelists: List<Foo>
}

val List<Bar>.serializationWhitelists
    get() = flatMapTo(LinkedHashSet(), Bar::serializationWhitelists) // OK in OI, NI: "Type checking has run into a recursive problem. Easiest workaround: specify types of your declarations explicitly"
