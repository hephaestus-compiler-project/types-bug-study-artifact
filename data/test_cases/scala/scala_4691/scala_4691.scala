trait Order {
   sealed trait EntryOption
   case object EmptyEntry extends EntryOption
   sealed trait Entry extends EntryOption
   private final class EntryImpl extends Entry
       
   def isEmpty( a: EntryOption ) : Boolean = a match {
      case EmptyEntry => true
//    case _: Entry   => false
   }
}
