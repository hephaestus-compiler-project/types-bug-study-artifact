class X {
  Y makeY() {
    new Y(a:1)
  }

  private class Y {
    int a
  }
}

println new X().makeY()
