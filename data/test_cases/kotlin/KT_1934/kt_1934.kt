trait Foo { fun get() : Integer; }
trait Bar { fun get() : String; }
trait Baz : Foo, Bar {} // Must be an ERROR
fun test(baz : Baz) : String { return baz.get(); }
