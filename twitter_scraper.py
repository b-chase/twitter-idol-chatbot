import twitter as tw
from twitter import TwitterHTTPError
from urllib.error import HTTPError
import re, time

access_token = "1061559864239910912-ft8g9lCsrC26rlK9FPoubZ3lIAnCIs"
access_secret = "YBIflHcBz1epCI5rUL1uApqyp4RSwTMXdGbYghT2putTZ"
consumer_key = "wJJc579miZHNyJJt9SwutD4nb"
consumer_secret = "QoexBqhop4pyACzbJUllp5NxnDwmb2EDxdKj6OvLJm9BAIwoBG"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAB9BKgEAAAAAIIlipt0CXlUQ%2FYLDI0tZwYMBifo%3DzGF1UY2ZOWuPFLGi3KIhM956EwbyEjSfIoc8xiRM1E5qGWQy4b"

twitter_handle = "benjaminwittes"
num_tweets = 20

t = tw.Twitter(auth=tw.OAuth(access_token, access_secret, consumer_key, consumer_secret))

big_list_of_tweets = t.statuses.user_timeline(screen_name=twitter_handle, include_rts=False, count=1000, tweet_mode='extended')
max_bulk = 100
sleeptime = 10
for i in range(max_bulk):
	print(f"Downloading tweets, part {i+1} of {max_bulk}")
	max_id = big_list_of_tweets[-1]["id"]-1
	try:
		big_list_of_tweets.extend(t.statuses.user_timeline(screen_name=twitter_handle, include_rts=False, count=1000, tweet_mode='extended', max_id=str(max_id)))
	except HTTPError or TwitterHTTPError:
		print(f"Twitter rate limit error. Sleeping for {sleeptime} seconds")
		time.sleep(sleeptime)
		sleeptime = int(sleeptime * 1.71)
	except:
		print(f"error downloading tweets, stopping at tweet #{i}")
		break
sleeptime = 60
with open("saved_tweets2.txt", "w") as savefile:
	for i, line in enumerate(big_list_of_tweets):
		# print(line)
		text = line['full_text']
		reply = line['in_reply_to_status_id_str']
		if (i+1) % 200 == 0:
			print(f"Currently on tweet {i} out of {len(big_list_of_tweets)}")
			print(f"Sleeping for {sleeptime} seconds to avoid hitting rate limit")
			time.sleep(sleeptime)
		if reply and len(re.findall(r"[^/s]", text)) > 0:
			try:
				leading_tweet = t.statuses.show(_id=reply, tweet_mode='extended')
				# print(f"leading: {leading_tweet['full_text']}")
				# print(f"response: {line['full_text']}")
				savefile.writelines([leading_tweet['full_text']+"\n", "+++||+++", line['full_text']+"\n", "+++||+++"])
			except UnicodeEncodeError:
				print(f"Line {i}: ", "Can't write this text to the file ")
				print(">>", leading_tweet['full_text'])
				print(">>", line['full_text'])
			except TwitterHTTPError as err:
				print(err.response_data)
				if err.response_data['errors'][0]['message'] == 'Rate limit exceeded':
					print("ending now")
					break
			except:
				print("Error, seems a tweet was deleted")
				print("Reply id:", reply)
