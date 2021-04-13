def runnable(Runnable r) {
    r.run()
}
def foo() {
    runnable { it -> // note explicit it
        println it
    }
}
foo()
