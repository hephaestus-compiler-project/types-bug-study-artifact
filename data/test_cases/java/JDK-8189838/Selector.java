interface Selector<E extends Enum<E> & Selector<E>> {}
    public void test2(){

        Map<String, Selector<?>> selectorMap = new HashMap<>();
        var sel = selectorMap.get("");
    }
