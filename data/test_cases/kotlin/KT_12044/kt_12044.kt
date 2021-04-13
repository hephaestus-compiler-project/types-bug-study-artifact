fun main(args: Array<String>) {
    val (x, y) =
                Pair(1,
                        if (1 == 1)
                            Pair<String, String>::first
                        else
                            Pair<String, String>::second)
}
