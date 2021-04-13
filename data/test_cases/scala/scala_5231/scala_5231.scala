object T {
  def m = new ConfigBuilder()
  implicit def build( cb: ConfigBuilder ) : Config = null
}

class Config(x: Int)

class ConfigBuilder private ()  { }
