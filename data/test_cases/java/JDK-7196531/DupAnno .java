import java.lang.annotation.*;
class DupAnno {
  void test() {
    @A @A String [] s;
  }
}