trait App(init: implicit Array[String] => Unit) {
  inline def main(args: Array[String]): Unit = init(args)
}
