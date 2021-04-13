class SealedExample
{
// Compiles if you remove `sealed` or if `I` is not generic
  sealed interface I<T> {
    final class C implements I<Object> { }
  }

  static void f(final I<Object> x) {
    if (x instanceof I.C) {

    }
  }
}
