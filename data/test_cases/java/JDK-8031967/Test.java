public class Test {
    private void test() {
        GroupLayout l = new GroupLayout();
        l.setHorizontalGroup(
            l.createParallelGroup()
                .addGroup(l.createParallelGroup())
                .addGap(1)
                .addComponent(new Object())
                .addGap(1)
                .addComponent(new Object()));
    }

    class GroupLayout {
        ParallelGroup createParallelGroup() {return null;}
        ParallelGroup createParallelGroup(int i) {return null;}
        ParallelGroup createParallelGroup(int i, int j) {return null;}
        void setHorizontalGroup(Group g) { }
    }

    class Group {
        Group addGroup(Group g) { return this; }
        Group addGroup(int i, Group g) { return this; }
        Group addGap(int i) { return this; }
        Group addGap(long l) { return this; }
        Group addGap(int i, int j) { return this; }
        Group addComponent(Object c) { return this; }
        Group addComponent(int i, Object c) { return this;}
    }

    class ParallelGroup extends Group {
        Group addGroup(Group g) { return this; }
        Group addGroup(int i, Group g) { return this; }
        Group addGap(int i) { return this; }
        Group addGap(int i, int j) { return this; }
        Group addComponent(Object c) { return this; }
        Group addComponent(int i, Object c) { return this; }
    }
}
