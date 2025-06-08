import requests
import json


class Post:
    def __init__(self, user_id: int, title: str, body: str):
        self.user_id = user_id
        self.title = title
        self.body = body


class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []
        global posts_repository
        for post in posts_repository.values():
            if post.user_id == self.id:
                self.posts.append(post)


    def average_title_length(self) -> float:
        if not self.posts:
            return 0.0
        total_length = sum(len(post.title) for post in self.posts)
        return total_length / len(self.posts)


    def average_body_length(self) -> float:
        if not self.posts:
            return 0.0
        total_length = sum(len(post.body) for post in self.posts)
        return total_length / len(self.posts)


class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []


    def fetch_data(self):
        get_users()
        get_posts_by_id()
        add_posts()
        add_users()
        self.users = list(users_repository.values())
        print('Data successfully fetched!')

    def user_with_longest_average_body(self) -> User:
        if not self.users:
            print("No users loaded.")
            return None

        max_user = max(self.users, key=lambda user: user.average_body_length())
        avg_length = max_user.average_body_length()
        print(f'User {max_user.name} has the longest average post body length - {avg_length} symbols!')
        return max_user


    def users_with_many_long_titles(self) -> list[User]:
        if not self.users:
            print("No users loaded.")
            return None

        users_with_titles = ''
        for i in posts_repository.values():
            my_user = users_repository[i.user_id]
            if len(my_user.posts) > 5 and len(i.title) > 40:
                if my_user.name in users_with_titles:
                    continue
                users_with_titles += f"{my_user.name}, "
        if users_with_titles:
            users_with_titles += '- users who have written more than 5 posts with titles longer than 40 characters'
            print(users_with_titles)
            return users_with_titles
        print('No users who have written more than 5 posts with titles longer than 40 characters')
        return None


# data fetching
users_info = []
posts_info = []
posts_repository = {}
users_repository = {}

def get_users():
    global users_info
    http_response_users = requests.get('https://jsonplaceholder.typicode.com/users')
    users_data = json.loads(http_response_users.content.decode())
    for i in users_data:
        users_info.append((i['id'], i['name']))

def get_posts_by_id():
    global posts_info
    global users_info
    import re
    for i in users_info:
        http_response_post = requests.get(f'https://jsonplaceholder.typicode.com/posts?userId={i[0]}')
        post_data = json.loads(http_response_post.content.decode())
        for j in post_data:
            body = j['body']
            posts_info.append((j['userId'], j['id'], j['title'], re.sub(r'\n', ' ', body)))

def add_posts():
    global posts_repository
    global posts_info
    for i in posts_info:
        posts_repository[i[1]] = Post(i[0], i[2], i[3])

def add_users():
    global users_repository
    global users_info
    for i in users_info:
        users_repository[i[0]] = User(i[0], i[1])


def main():
    instrument_for_analysis = BlogAnalytics()
    print("Welcome to Blog Analytics 3000! Commands to get started: \nfetch - to fetch data from blog. Use it before"
          " using the other commands\n"
          "longest body - show user with with the longest average post body length\n"
          "long titles - show all users who have written more than 5 posts with titles longer than 40 characters\n"
          "quit - to quit the Blog Analytics 3000")
    while True:
        command = input('\nEnter the command: ')

        match command:
            case 'fetch':
                instrument_for_analysis.fetch_data()
            case 'longest body':
                instrument_for_analysis.user_with_longest_average_body()
            case 'long titles':
                instrument_for_analysis.users_with_many_long_titles()
            case 'quit':
                print('Thanl you for using Blog Analytics 3000!')
                break
            case _:
                print("Wrong command!")


if __name__ == '__main__':
    main()

