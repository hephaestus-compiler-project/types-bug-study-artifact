import java.util.*;

interface Predicate<T> {
   void m(T t);
}

interface Stream<T> {
   void forEach(Predicate<T> pt);
}

 

class Crash<U> {

    public void crash(U current, Stream<U> stream) {
        List<U> list3 = new ArrayList<>();

        stream.forEach(i -> list3.add(current.clone()));

    }
}