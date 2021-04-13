class ListCompilerAndReverser {
  static List<Integer> revlist(List<List<String>> list) {
    List<Integer> intermediate = list.collectMany { strings ->
      List<Integer> result = strings.collect {
        it.toInteger()
      }
      result
    }
    intermediate.sort { int it ->
      -it
    }
  }
}
