class Foo {
	String method() {
		return callT('abc')
	}

    private <T> T callT(T t) {
		return callV(t)
	}

	private <V> V callV(V v) {
		return v
	}
}

println new Foo().method()
