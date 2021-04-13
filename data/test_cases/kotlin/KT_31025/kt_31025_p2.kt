fun actualTest(inv: Inv<String>) {
    val m: ((String) -> String) -> Inv<String> = inv::map // Error in NI, ok in OI
}
