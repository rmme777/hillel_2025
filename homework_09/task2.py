import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

class CommentModerator:
    BAN_WORDS = ['free', 'buy', 'offer']
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        try:
            response = requests.get(f"{BASE_URL}/comments")
            json_data = response.json()
            for i in json_data:
                comment = Comment(i['id'], i['postId'], i['name'], i['email'], i['body'])
                self.comments.append(comment)
        except Exception as error:
            print('Error:', error)

    def flag_suspicious_comments(self):
            comments_by_user = {}

            for comment in self.comments:
                email = comment.email
                body = comment.body.lower().strip()
                if email not in comments_by_user:
                    comments_by_user[email] = {}
                if body not in comments_by_user[email]:
                    comments_by_user[email][body] = []
                comments_by_user[email][body].append(comment)

            self.flagged_comments = []
            for email, body_dict in comments_by_user.items():
                for body, comments_list in body_dict.items():
                    has_ban_word = any(word in body for word in CommentModerator.BAN_WORDS)
                    if has_ban_word:
                        self.flagged_comments.extend(comments_list)
                    else:
                        if len(comments_list) > 1:
                            self.flagged_comments.extend(comments_list)

            print("\nSummary report of number of flagged comments per post:")
            grouped = self.group_by_post()
            if grouped:
                for post_id, comments in grouped.items():
                    print(f"Post ID {post_id}: {len(comments)} flagged comments")
            else:
                print('0 flagged comments')

    def group_by_post(self) -> dict[int, list[Comment]]:
        grouped_comments = {}
        for comment in self.flagged_comments:
            post_id = comment.post_id
            if post_id not in grouped_comments:
                grouped_comments[post_id] = []
            grouped_comments[post_id].append(
                Comment(comment.id, comment.post_id, comment.name, comment.email, comment.body)
            )
        return grouped_comments


    def top_spammy_emails(self, n: int = 5) -> list[str]:
        email_counts = {}
        for comment in self.flagged_comments:
            email = comment.email
            if email not in email_counts:
                email_counts[email] = 1
            else:
                email_counts[email] += 1

        sorted_emails = sorted(email_counts.items(), key=lambda x: x[1], reverse=True)
        top =  [email for email, count in sorted_emails[:n]]

        print(f"\ntop-{n} spammy emails:")
        if top:
            for email in top:
                count = sum(1 for c in self.flagged_comments if c.email == email)
                print(f"{email}: {count} flags")
        else:
            print("0 spammy emails")


    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        json_data = []
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for i in self.flagged_comments:
                    json_data.append({'id': i.id, 'postId': i.post_id, 'name': i.name, 'email': i.email, 'body': i.body})
                json.dump(json_data, file, ensure_ascii=False, indent=4)
                print("\nData exported successfully.")
        except Exception:
            print('\nSomething went wrong while exporting the data.')

s = CommentModerator()
s.fetch_comments()
s.flag_suspicious_comments()
s.top_spammy_emails()
s.export_flagged_to_json()
