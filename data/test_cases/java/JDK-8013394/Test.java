import pkg.TestCollection;

public class Test {
    public static void main(String[] args) {
        TestCollection<String>  tc1 = new TestCollection<String>();
        for (String s : tc1) {
           System.out.println(s);
        }
      }
}
