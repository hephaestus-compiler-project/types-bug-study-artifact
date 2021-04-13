/**
 * A utility class for comparing two maps
 */
class MapComparison implements Iterable<IntegerPair> {
    Map<String, Integer> m1
    Map<String, Integer> m2
    Set<String> unionKeys = null

    MapComparison(Map<String, Integer> map1, Map<String, Integer> map2) {
        this.m1 = map1
        this.m2 = map2
    }

    @Override
    Iterator<IntegerPair> iterator() {
        if (unionKeys == null) {
            unionKeys = m1.keySet() + m2.keySet()
        }
        return new IntegerPairIterator(unionKeys.iterator())
    }

    class IntegerPairIterator implements Iterator<IntegerPair> {
        private Iterator<String> keyIterator

        IntegerPairIterator(Iterator<String> keyIterator) {
            this.keyIterator = keyIterator
        }

        @Override
        boolean hasNext() {
            return keyIterator.hasNext()
        }

        @Override
        IntegerPair next() {
            String key = keyIterator.next()
            IntegerPair comp = new IntegerPair(m1[key], m2[key])
            return comp
        }

        @Override
        void remove() {
            throw new UnsupportedOperationException()
        }
    }

    static class IntegerPair  {
        Integer i1;
        Integer i2;

        IntegerPair(Integer int1, Integer int2) {
            i1 = int1;
            i2 = int2;
        }
    }
}

def mc = new MapComparison([:],[:])
