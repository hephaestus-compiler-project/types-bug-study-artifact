interface Task<E extends Exception> {}
class Comparator<T> {}
class CustomException extends Exception {}

class TaskQueue<E extends Exception, T extends Task<E>> {}

abstract class Test {
    abstract <E extends Exception, T extends Task<E>> TaskQueue<E, T> create(Comparator<? super T> comparator);

    void f(Comparator<Task<CustomException>> comp) {
        TaskQueue<CustomException, Task<CustomException>> queue = create(comp);
    }
}