class GC {
    void setStrings(List<String> ss) {}
}

void usage(GC gc) {
    gc.strings = Collections.emptyList()
}
