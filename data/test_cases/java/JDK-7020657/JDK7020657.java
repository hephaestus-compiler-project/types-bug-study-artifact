import java.util.*;

interface A {
int get(List<String> l);
}

interface B {
int get(List<Integer> l);
}

interface C extends A, B { // Don't forget the extends clause!
int get(List l);
}