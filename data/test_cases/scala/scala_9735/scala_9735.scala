trait Two[A, B]

opaque type U[A] = [B] =>> Two[A, B] // compiles fine
opaque type T[A] = [B] =>> String // error :(
