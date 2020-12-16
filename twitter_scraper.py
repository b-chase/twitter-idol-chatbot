import twitter as tw
from twitter import TwitterHTTPError
from urllib.error import HTTPError
import re
import time

# In order to use this program you must sign up to be a twitter developer 
# and obtain access to their API with the following tokens:
try:
    from twitter_keys import access_secret, access_token, consumer_key, consumer_secret
except ImportError:
    access_token = ""
    access_secret = ""
    consumer_key = ""
    consumer_secret = ""
    bearer_token = ""

t = tw.Twitter(auth=tw.OAuth(access_token, access_secret, consumer_key, consumer_secret))


def pull_and_save_tweets(twitter_handle):
    big_list_of_tweets = t.statuses.user_timeline(screen_name=twitter_handle,
                                                  include_rts=False,
                                                  count=1000,
                                                  tweet_mode='extended')
    max_bulk = 500
    sleep_time = 120
    for i in range(max_bulk):
        print(f"Downloading tweets, part {i + 1} of {max_bulk}")
        max_id = big_list_of_tweets[-1]["id"] - 1
        try:
            big_list_of_tweets.extend(
                t.statuses.user_timeline(screen_name=twitter_handle,
                                         include_rts=False,
                                         count=1000,
                                         tweet_mode='extended',
                                         max_id=str(max_id)))
        except HTTPError or TwitterHTTPError:
            print(f"Twitter rate limit error. Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
            sleep_time = int(sleep_time * 1.71)
        except:
            print(f"error downloading tweets, stopping at tweet #{i}")
            break
    time.sleep(sleep_time)
    sleep_time = 60
    with open(f"{twitter_handle}_tweets.txt", "w") as savefile:
        print(f"Saving file as '{savefile.name}'")
        for i, line in enumerate(big_list_of_tweets):
            # print(line)
            text = line['full_text']
            reply = line['in_reply_to_status_id_str']
            if (i + 1) % 100 == 0:
                print(f"Currently on tweet {i + 1} out of {len(big_list_of_tweets)}")
                print(f"Sleeping for {sleep_time} seconds to avoid hitting rate limit")
                time.sleep(sleep_time - 30)
                print("30 seconds left to wait")
                time.sleep(30)
            if reply and len(re.findall(r"[^/s]", text)) > 0:
                try:
                    leading_tweet = t.statuses.show(_id=reply, tweet_mode='extended')
                    # print(f"leading: {leading_tweet['full_text']}")
                    # print(f"response: {line['full_text']}")
                    savefile.writelines(
                        [leading_tweet['full_text'] + "\n", "+++||+++", line['full_text'] + "\n", "+++||+++"])
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
    return


pull_and_save_tweets("benjaminwittes")
