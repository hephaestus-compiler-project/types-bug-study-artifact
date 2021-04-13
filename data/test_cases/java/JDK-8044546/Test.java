import java.util.Arrays;
                                                                                                                                      
public class Test
{
        public boolean asd(Object[] data)
        {
                return Arrays.stream(data).reduce(true, (a,b) -> a && b.length == len, (a,b) -> true);
        }
}