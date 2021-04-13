class Foo { var bar = 0 }

def test1(f: Foo): Unit = {
  import f.{bar => baz}
  baz += 1  // does not compile
}

def test2(f: Foo): Unit = {
  import f.{bar => baz, bar_= => baz_=}
  baz += 1  // does not compile
}
