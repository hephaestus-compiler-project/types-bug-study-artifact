@groovy.transform.CompileStatic
public class A<T extends List<E>, E extends Map<String, Integer>> {
    E getFirstRecord(T recordList) {
        return recordList.get(0);
    }
}
