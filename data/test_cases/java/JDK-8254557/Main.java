import java.sql.ResultSet;
import java.util.Iterator;
import java.util.function.Function;
import java.util.stream.Stream;

public class Main
{
    public static void main(String[] args)
    {
    }

    public <T> Stream<T> stream(Class<T> clazz)
    {
        return stream(rs->{
            if (null != clazz)
            {
                return new Iterator<>()
                {
                    @Override
                    public boolean hasNext()
                    {
                        return true;
                    }

                    @Override
                    public T next()
                    {
                        return null;
                    }
                };
            }
            else
            {
                return new Iterator<>()
                {
                    @Override
                    public boolean hasNext()
                    {
                        return true;
                    }

                    @Override
                    public T next()
                    {
                        return null;
                    }
                };
            }
        });
    }

    private static <T> Stream<T> stream(Function<ResultSet, Iterator<T>> function)
    {
        return null;
    }
}
