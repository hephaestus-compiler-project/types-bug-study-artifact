class Bug1Base<T> {
    T t
    T get(a, b=0) {
        return t
    }
}
Bug1Base<Integer> bug = new Bug1Base<Integer>(t:1)
Integer t = bug.get(1)
println t
