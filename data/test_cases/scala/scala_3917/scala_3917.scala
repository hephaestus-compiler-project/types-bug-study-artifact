class Hello {
  var verbose = false
}

object Main extends Hello {
  def test = {
    verbose = true
  }
}
