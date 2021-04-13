class Thing {

  public <O> void contravariant(Class<? super O> type, O object) {}
  public <O> void invariant(Class<O> type, O object) {}

  void m() {
    invariant(String, "foo")
    contravariant(String, "foo") // fails, can't find method
  }
}
