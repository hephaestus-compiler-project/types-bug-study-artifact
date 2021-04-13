import java.nio.file.StandardCopyOption

enum TestEnum {
    A, B, C
}

class TestGenerics {
    public static <T> List<T> randomSample(T[] sequence) {
        return Arrays.asList(sequence)[0..1]
    }

    def test1 = randomSample(TestEnum.values())
    def test2 = randomSample(StandardCopyOption.values())
}
