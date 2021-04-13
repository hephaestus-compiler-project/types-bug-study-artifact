object Main {
  def fun(op: implicit erased (Int) => Unit) = op(0)
  fun { }
}
