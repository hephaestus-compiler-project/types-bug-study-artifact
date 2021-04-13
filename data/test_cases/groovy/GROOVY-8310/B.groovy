@CompileStatic
class B {
    public <T> T bar(Closure<Collection<Integer>> a) {
        return null
    }

    def use() {
       bar {
            [1]
        }
    }
}
