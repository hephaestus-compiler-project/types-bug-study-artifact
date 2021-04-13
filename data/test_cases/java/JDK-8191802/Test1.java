class A<T extends Number> {}

public class Test1 {
    public void run() {
        A<? super Integer> a0 = new A<Integer>();
        var c0 = a0;
        A<? super Integer> tmp = c0;
    }
}
