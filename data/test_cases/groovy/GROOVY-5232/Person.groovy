class Person {
    String name

    static Person create() {
        def p = new Person()
        p.setName("Guillaume")
        // but p.name = "Guillaume" works
        return p
    }
}

Person.create()
