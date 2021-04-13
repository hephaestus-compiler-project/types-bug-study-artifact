class A(a: Any) { 
  def this() = {  
    this(b)       
    lazy val b = new {}
  }
}
