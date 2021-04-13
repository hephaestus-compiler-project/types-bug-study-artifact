/**
 * @test
 * @compile Bar.java Super.java
 * @clean p.Super
 * @compile CFInImport.java
 */
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Retention;

import static p.Bar.CONST;

@Retention(RetentionPolicy.RUNTIME)
@interface Foo {}