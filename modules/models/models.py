class Submission:
    def __init__(self, _id, subreddit, title, author, upvotes, downvotes, timePosted):
        self.id = _id
        self.subreddit = subreddit
        self.author = author
        self.upvotes = upvotes
        self.title = title
        self.downvotes = downvotes
        self.timePosted = timePosted

class Comment:
    def __init__(self, _id, subreddit, parentPost, upvotes, downvotes, author, content, time):
        self.id = _id
        self.subreddit = subreddit
        self.parentPost = parentPost
        self.downvotes = downvotes
        self.upvotes = upvotes
        self.author = author
        self.content = content
        self.time = time
