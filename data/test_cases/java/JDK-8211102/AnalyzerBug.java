import java.util.*;

public class AnalyzerBug {
    private void t(boolean b) {
        (b ? Collections.emptyList() : new Iterable<String>() { public Iterator<String> iterator() { return null; } }).toString();
    }
}