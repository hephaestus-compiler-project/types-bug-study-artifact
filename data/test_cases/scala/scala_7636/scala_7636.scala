object Main extends App{
  class ResultTable[E]( query : Either[_,E] )( columns : Int )
  class C extends ResultTable(Left(5):Either[_,_])(5)
}
