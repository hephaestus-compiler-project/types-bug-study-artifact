 interface I<X1,X2> {}
  class C<T> implements I<T,T> {}

  <X> void m(I<? extends X, X> arg) {}

  void test(C<?> arg) {
    m(arg);
  }
