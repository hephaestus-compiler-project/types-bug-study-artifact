def foo[S <: String]: String => Int = new { def apply(s: S): Int = 0 }
val test = foo("")
