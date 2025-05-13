"""
About the code:

`users` list includes multiple users (define them by yourself)
`command()` is only a single function that mimics the business logic
`auth()` is a decorator that requires user authorization to perform tasks


NOTES
"""

class User:
    users = {}
    def __init__(self, username, password):
        self.username = username
        self.password = password
        User.users[self.username] = self.password

user1 = User("coolguy", "guy4501")
user2 = User("kartipop21", "lpapal091")
user3 = User("the_average_user", "hardpassword1")



def auth(func):
    def wrapper(*args, **kwargs):
        print("=====================================\nВам нужно авторизоваться!\nВведите имя пользователя и пароль"
              "\n=====================================")
        while True:
            username = input("Введите имя пользователя: ")
            if username in User.users:
                password = input("Введите пароль: ")
                if password == User.users[username]:
                    print("Авторизация прошла успешно!")
                    print('=====================================')
                    return func(*args, **kwargs)
                else:
                    print("Неверный пароль")
            else:
                print("Пользователь не найден")
    return wrapper


@auth
def command(payload):
    print(f"Executing command by authorized user.\nPayload: {payload}")


def main():
    while True:
        user_input = input("Enter anything: ")
        command(user_input)
        break

if __name__ == '__main__':
    main()