type YZ = [Y[_]] => [Z[_]] => [T] => Y[Z[T]]
val l: YZ[List][List][Int] = List(List(1))
