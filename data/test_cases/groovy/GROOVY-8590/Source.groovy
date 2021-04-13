class Source {
    Object getValue() { '32' }
}
int m(Source src) {
    return Integer.parseInt((String) src.getValue())
}
