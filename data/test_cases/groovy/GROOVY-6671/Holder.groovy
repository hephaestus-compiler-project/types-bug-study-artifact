// Note: this interface must be in different script because of GROOVY-6670
interface Converter<F, T> {
  T convert(F from)
}

class Holder<T> {
  T thing

  Holder(T thing) {
    this.thing = thing
  }

  def <R> Holder<R> convert(Converter<? super T, ? extends R> func1) {
    new Holder(func1.convert(thing))
  }
}

void m() {
  new Holder<Integer>(2).convert {
    it
  } convert {
    it.floatValue() // fails, doesn't know 'it' is an Integer
  }
}

m()
