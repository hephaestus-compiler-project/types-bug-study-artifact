trait MyTrait {
    val a: Int
}

class MyTraitImpl: TraitJavaImpl() 

fun main(args: Array<String>) {
    MyTraitImpl().a
}
