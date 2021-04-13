import java.util.*;

interface A { List<Number> getList(); }
interface B { List getList(); }
interface AB extends A, B {}

class Test {
   void test(AB ab) {
      Number n = ab.getList().get(1); //error here
   }
}
