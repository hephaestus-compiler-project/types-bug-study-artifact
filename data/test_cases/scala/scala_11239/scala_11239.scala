trait Request[F[_]]
final case class AuthedRequest[F[_], A](authInfo: A, req: Request[F])
trait Context { type F[_] }
final case class HttpRequestContext[C <: Context, Ctx](request: AuthedRequest[C#F, Ctx], context: Ctx)
