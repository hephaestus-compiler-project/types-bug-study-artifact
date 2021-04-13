object Test {
  type Snd[t[_[_, _]]] = t[[a, b] => b]

  class Witness[t[_[_, _]]](value: Snd[t]) {
    def foo[t[_[_, _]]](value: Snd[t] = value) = {}
  }
}
