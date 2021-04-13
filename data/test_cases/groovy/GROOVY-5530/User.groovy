class User {
    String login
    String username
    String domain
    String firstName
    String lastName
}
class UserBase {
    List<User> getUsers() {
        [1, 2, 3].collect { Number num ->
             new User(
                    login:      "login$num",
                    username:   "username$num",
                    domain:     "domain$num",
                    firstName:  "first$num",
                    lastName:   "last$num"
            )
        }
    }
}
def users = new UserBase().getUsers()
