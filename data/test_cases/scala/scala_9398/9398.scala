sealed abstract class TA
sealed abstract class TB extends TA
case object B extends TB
case object B2 extends TB

case class CC(i: Int, tb: TB)

// Should warn that CC(_, B2) isn't matched
val test: CC => Unit = {
  case CC(_, B) => ()
}
