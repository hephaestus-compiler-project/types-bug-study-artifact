public <T> void someMethod (java.lang.Class<T> clazz, T object) {}

void method() {
  List<String> list = null
  someMethod(java.util.List.class, list)
}

new MyClass().method()
