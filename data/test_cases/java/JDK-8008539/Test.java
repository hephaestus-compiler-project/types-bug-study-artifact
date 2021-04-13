import java.util.*;

interface SAM {
    Object m();
}

class Test {
    SAM s = SAM::new;
}