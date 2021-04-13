int len(byte[] arr) { arr.length }
def foo(arg) {
   if (arg instanceof byte[]) {
      len(arg)
   }
}
foo(new byte[3])
