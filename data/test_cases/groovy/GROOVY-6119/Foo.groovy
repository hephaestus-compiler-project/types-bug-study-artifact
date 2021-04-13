class Foo {
   String message
   Foo(Map map) {
      message = map.msg
   }
}
def foo = new Foo(msg: 'bar')
assert foo.message == 'bar'
