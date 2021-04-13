interface  X<T> {
    // (1) Error:(5, 5) Kotlin: Modifier 'inner' is not applicable to 'enum class'
    // (2) Error:(5, 28) Kotlin: Expression is inaccessible from a nested class 'C', 
    //       use 'inner' keyword to make the class inner
    inner enum class C : X<T>
}
