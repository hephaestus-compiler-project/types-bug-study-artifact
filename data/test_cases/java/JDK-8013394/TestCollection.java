package pkg;
import java.util.Iterator;
import java.util.NoSuchElementException;
public class TestCollection<E> implements Iterable<E> {
    public testCollectionIterator iterator() {
        return  new testCollectionIterator();
    }
    class testCollectionIterator implements Iterator<E> {
       public boolean hasNext() { return true; }
        public E next() throws NoSuchElementException"
       {
          return null;
        }
       public void remove() {}
    }
}
