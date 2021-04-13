class Test {

    public void traverse() {
        println new Node_().class.name
        for (/*Object*/Node_ node : new MyTraverser().nodes()) {
            println node.class.name
        }
    }
}

class Node_ {}

interface Traverser {

    Iterable<Node_> nodes();
}

class MyTraverser implements Traverser {

    @Override
    Iterable<Node_> nodes() {
        []
    }
}
