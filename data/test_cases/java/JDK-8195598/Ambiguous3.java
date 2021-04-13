public class Ambiguous3 {
    public CompletableFuture<?> test() {
        return ok(() -> System.out.append("aaa"));
    }
    public <T> CompletableFuture<T> ok(Supplier<T> action) {
        return CompletableFuture.supplyAsync(action);
    }
    public <T> CompletableFuture<T> ok(T body) {
        return CompletableFuture.completedFuture(body);
    }
    public CompletableFuture<Void> ok(Runnable action) {
        return CompletableFuture.runAsync(action);
    }
}
