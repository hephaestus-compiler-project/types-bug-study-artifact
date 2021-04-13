class Gr {
    void f1(Object obj) {
        if (!(obj instanceof Runnable)) {
            return
        }
        f3(obj) // failed compiled here  : Cannot find matching method Gr#f3(java.lang.Object).
    }

    void f3(Runnable r) {  }
}
