def m(def obj) {
  def isA = (obj instanceof String && obj.equalsIgnoreCase('a'))
  obj.toLowerCase() // should be STC error; if above line is commented out, error shows
}
