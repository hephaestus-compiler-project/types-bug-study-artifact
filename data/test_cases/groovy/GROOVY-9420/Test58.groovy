public class Test58 {

	Map<String, String> m = [
		foo: 'foo'
		]

	void blah() {
		Object c = boh()
		def a = m.get(c)
		uhuh(a)
		def b = m[c]
		uhuh(b)
	}

	void uhuh(String a) {
	}

	Object boh() {
		'foo'
	}
}
