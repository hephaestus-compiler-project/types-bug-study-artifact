public class Test {
    class Base {
        protected int i = 1;
     }

    class Sub extends Base {
        void func() {
            Sub.super.i += 10;
        }
    }
}