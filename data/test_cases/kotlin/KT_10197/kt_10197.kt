interface ILeft {
    fun foo(): ILeft
}

interface IRight {
    fun foo(): IRight
}

class CBoth : ILeft, IRight {
    override fun foo(): CBoth = CBoth()
}

class CX : ILeft by CBoth(), IRight
