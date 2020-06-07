# Tweeter bot based on https://www.makeuseof.com/tag/build-social-media-bots-python/

import tweepy
from credentials import *

tw_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
tw_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
tw_api = tweepy.API(tw_auth)

# Creating a tweet
for tweet in tweepy.Cursor(tw_api.search,q='MakeUseOf').items(10):
	try:
		tweet.favorite()
		tweet.retweet()
		time.sleep(2)
	except tweepy.TweepError as e:
		print(e.reason)
	except StopIteration:
		break

# Search Reddit and Instagram for new posts and tweet them
# use r/<hashtag> for reddit search
# and #<hashtag> for instagram search
hashtag = 'technology'
num_posts = 5

# tweet reddit info
reddit_posts = my_reddit.subreddit(hashtag).new(limit=num_posts)
for submission in reddit_posts:
	title = submission.title
	url = 'www.reddit.com{}'.format(submission.permalink)
	tweet_str = f'Reddit r/{sub} update:\n\n{title} #{sub} {url}'
	tweet_str = trim_to_280(tweet_str)
	tw_api.update(tweet_str)

# tweet instagram media
media_info = get_images_from_hashtag(hashtag, num_posts)
for (filename, message) in media_info:
	try:
		tweet_str = trim_to_280(message)
		tw_api.update_with_media(filename, status=tweet_str)
	except tweepy.TweepError as e:
		print(e.reason)
	except StopIteration:
		break
