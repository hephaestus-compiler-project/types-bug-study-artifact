abstract class Base<A extends Base<A>> {}
class Done extends Base<Done> { }
class Next<H, T extends Base<T>> extends Base<Next<H, T>> {
  H head; T tail
  static Next<H, T> next(H h, T t) { new Next<H, T>(head:h, tail:t) }
  String toString() { "Next($head, ${tail.toString()})" }
}
import static Next.*

def foo() {
  Next<Integer, Next<String, Done>> x = next(3, next("foo", new Done()))
}

println foo() // => Next(3, Next(foo, Done@9b3ec2))
