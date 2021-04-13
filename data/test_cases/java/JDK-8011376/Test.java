import java.util.*;

class Test {
Callable<Number> tasks = id(id(()->{ if (true) throw new java.io.IOException(); else return 0; }));

<Z> Z id(Z z) { return null; }

}
