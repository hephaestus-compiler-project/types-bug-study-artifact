import java.util.*;
 
public class X {
    static interface Foo {
    }
 
    public static void main(String[] args) {
        List<Date> list = new ArrayList<>();
        list.add(new Date());
 
        List<Foo> cList = (List<Foo>) (List<?>) list;
        Date date = (Date) cList.get(0);
    }
}