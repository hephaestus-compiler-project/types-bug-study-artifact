public class Foo {
    private List<String> names;
    public List<String> getNames() {
        return names;
    }
    public void setNames(List<String> names) {
        this.names = names;
    }
}
class FooWorker {
    public void doSomething() {
        new Foo().with {
            names = new ArrayList()
        }
    }
}
new FooWorker().doSomething()
