fun case3(x: Any){
   when (x){
       1 -> try { {"1"}}catch (e: Exception) { { }} //Type mismatch.
       "1" -> try { 1 }catch (e: Exception) { { }} //Type mismatch.
       else -> try { 1 }catch (e: Exception) { {1 }} //Type mismatch.
   }
}
