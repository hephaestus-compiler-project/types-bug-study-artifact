interface SamType {
    int sam()
}

int foo(SamType samt) {
    samt.sam()
}

assert foo { -> 1 } == 1
