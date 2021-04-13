import java.lang.annotation.ElementType;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Target;

@Target({ElementType.TYPE_USE})
@Repeatable(FooContainer.class)
@interface Foo {}

@Target({ElementType.TYPE, ElementType.TYPE_USE})
@interface FooContainer {
   Foo[] value();
}
