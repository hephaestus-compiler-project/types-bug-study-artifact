interface ThrowableRunnable<E extends Throwable> {
    void compute() throws E;
}

public abstract class Overloads {

    public abstract < E extends Exception> void computeException(ThrowableRunnable<E> process) throws E;


    public static <T, E extends Throwable> T compute(ThrowableRunnable<E> action) throws E {
        return null;
    }

    {
        computeException(() -> compute(() -> {}));
    }
}