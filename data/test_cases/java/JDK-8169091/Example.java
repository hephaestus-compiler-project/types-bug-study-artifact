import java.io.Serializable;
import java.util.Comparator;

interface Example {
    static <T extends Comparable<? super T>> Comparator<T> comparator() {
        return (Comparator<T> & Serializable)T::compareTo;
    }
}
