@Grab(group='com.netflix.rxjava', module='rxjava-core', version='0.18.1')
import rx.Observable
import java.util.concurrent.Callable

class Example {

  static <T> Observable<T> observe(Callable<Iterable<T>> callable) {
    Observable.from(callable.call())
  }

  static void main(String[] args) {
    observe({ ["foo"] }) map {
      it.toUpperCase() // <- compiler doesn't know 'it' is a string
    } subscribe {
      println it
    }
  }
}
