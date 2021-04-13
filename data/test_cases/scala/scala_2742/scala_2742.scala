object Test {
  class A
  class B
  implicit def a2b(x: A): B = new B
  
  abstract class C1 { def f: B }
  
  class C2 extends C1 { def f = new A }     // compiles
  class C3 extends C1 { val f: B = new A }  // compiles
  
  // a.scala:16: error: overriding method f in class C1 of type => Test.B;
  //  value f has incompatible type
  //   class C4 extends C1 { val f = new A }
  //                             ^
  class C4 extends C1 { val f = new A }
}
