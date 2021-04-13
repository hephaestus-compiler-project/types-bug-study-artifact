['a','bb','ccc'].inject(0) { int acc, String str -> acc += str.length(); acc }
