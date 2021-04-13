import java.util.*;

class Bug {
  public static <V> Set<V> copy(final Set<? extends V> set) {
    return new HashSet<>(set);
  }
}
