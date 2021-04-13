import java.lang.annotation.*;
import java.util.function.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE_USE)
@interface TA {}

class LambdaFormal {
   IntUnaryOperator x = (@TA int y) -> 1;
}
