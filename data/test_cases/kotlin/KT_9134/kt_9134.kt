fun bar(): Int = {
    var i: Int?
    i = 42
    // smart cast
    i.hashCode() 
    // type mismatch; with i!! we have "unnecessary not null assertion" instead
    i 
}()
