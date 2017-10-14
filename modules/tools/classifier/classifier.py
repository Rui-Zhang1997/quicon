'''
This is the meat of the project. The goal is to pull news stories from a number of subreddits,
analyze the contents of the comments, analyze the general sentiment of the article, its users,
political leaning, etc. It will hopefully be able to tell us a few things:
    1. What are the most popular topics for those subreddits
    2. Are comments usually LRoC?
    3. Are their more upvotes or downvotes on comments that are LRaC
    4. Who are more active on reddit in general, LRoC?
    5. What are the leaning of the sources used, LRoC?

Method - Primitive:
    For each subreddit, we pull the top 20 hottest posts of that present time, as well
    as 10 random posts from the top 100, and gather a few pieces of data:
        1. Source
        2. Title
        3. Who commented
        4. Do the people who comments post on political subreddits with what leaning
        5. Are the reactions to their posts negative or positive
    From this we can gather some information regarding what people are feeling and
    who visits those subreddits.

This kind of builds off of Max Candocia's work.
'''


