inline fun <ERR : ErrorCode, A, B, C, D, E, F, G, H, I, J, R> apply(fn: (A, B, C, D, E, F, G, H, I, J) -> R, a: Result<ERR, A>, b: Result<ERR, B>, c: Result<ERR, C>, d: Result<ERR, D>, e: Result<ERR, E>, f: Result<ERR, F>, g: Result<ERR, G>, h: Result<ERR, H>, i: Result<ERR, I>, j: Result<ERR, J>): Result<ERR, R> =
            a.flatMap { aValue: A ->
                b.flatMap { bValue: B ->
                    c.flatMap { cValue: C ->
                        d.flatMap { dValue: D ->
                            e.flatMap { eValue: E ->
                                f.flatMap { fValue: F ->
                                    g.flatMap { gValue: G ->
                                        h.flatMap { hValue: H ->
                                            i.flatMap { iValue: I ->
                                                j.flatMap { jValue: J ->
                                                    success(fn(aValue, bValue, cValue, dValue, eValue, fValue, gValue, hValue, iValue, jValue))
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
