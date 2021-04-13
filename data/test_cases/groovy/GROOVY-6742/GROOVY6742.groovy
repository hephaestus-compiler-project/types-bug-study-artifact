public static <F, T> FutureCallback<F> deferredCallback(DeferredResult<T> deferredResult, final Function<F, T> function) {
    return new FutureCallback<F>() {
        @Override
        void onSuccess(F result) {
            deferredResult.setResult(function.apply(result))
        }
    };
}
