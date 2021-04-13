abstract class Parent<T> {
    public T value
}
class Impl extends Parent<Integer> {}
Impl impl = new Impl()
Integer i = impl.value
