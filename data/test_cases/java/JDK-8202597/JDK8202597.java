class JDK8148354 {
    interface I {}
    interface J { void foo(); }

    public void test() {
        Object o1 = (I & J) System::gc;
        Object o2 = (Object & J) System::gc; 
        Object o3 = (Object & I & J) System::gc;
    }
}
