import groovy.transform.CompileStatic

@CompileStatic
class BugTest {
    private class CompilerKiller<T> {
        private T t
        public CompilerKiller(T t){
            this.t = t
        }
    }

    public void "This causes a NPE"(){
        CompilerKiller<BugTest> sample = new CompilerKiller<>(this)
    }

    public void "This causes a NPE as well"(){
        CompilerKiller<BugTest> sample = new CompilerKiller<>(new BugTest())
    }

    public void "This does work"(){
        CompilerKiller<BugTest> sample = new CompilerKiller<BugTest>(this)
    }