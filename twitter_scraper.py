from twitter import Api
from urllib.error import HTTPError
import re
import time

# In order to use this program you must sign up to be a twitter developer 
# and obtain access to their API with the following tokens:
try:
    from twitter_keys import access_secret, access_token, consumer_key, consumer_secret
    from twitter_keys import interest_list
except ImportError:
    access_token = ""
    access_secret = ""
    consumer_key = ""
    consumer_secret = ""


api = Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
          access_token_key=access_token, access_token_secret=access_secret)
text_key = "text"
if True:
    api.tweet_mode = "extended"
    text_key = "full_text"

# print(api.VerifyCredentials())
def get_older_tweets(handle, max_id=None, count=200):
    url = "%s/statuses/user_timeline.json" % api.base_url
    result = []
    parameters = {
        "screen_name": handle,
        "count": count
    }
    if max_id:
        parameters["max_id"] = max_id
    resp = api._RequestUrl(url, 'GET', data=parameters)
    pulled_tweets = api._ParseAndCheckTwitter(resp.content.decode('utf-8'))
    return pulled_tweets

def pull_and_save_tweets(twitter_handle, bulk_calls=100):
    tweet_list = get_older_tweets(twitter_handle)
    prev_length = len(tweet_list)
    id_max = tweet_list[-1]["id"] - 1
    for i in range(1, bulk_calls):
        print(f"Have {(bulk_calls - i) * 200} tweets left to pull. The new max ID is: {id_max}")
        tweet_list.extend(get_older_tweets(twitter_handle, id_max))
        id_max = tweet_list[-1]["id"] - 1
        if len(tweet_list) == prev_length:
            print("Out of tweets!")
            break
        prev_length = len(tweet_list)
    print(f"Pulled a total of {prev_length} tweets for {twitter_handle}. Last tweet:")
    print(tweet_list[-1])
    quote_convos = []
    reply_convos_dict = {}
    print("Finished getting bulk tweets. Getting replied-to and quoted tweets now")
    for tweet in tweet_list:
        # print(tweet.keys())
        a_status = tweet.get("id")
        q_status = tweet.get("in_reply_to_status_id")
        if not q_status:
            q_status = tweet.get("quoted_status_id")
            if not q_status:
                continue
            quote_convos.append((tweet.get("quoted_status", {text_key: "NOQUOTEDSTATUS"}).get(text_key, "NOQUOTEDTEXT"), tweet[text_key]))
            # print("quoted convo:", quote_convos[-1])
        reply_convos_dict[q_status] = tweet.get(text_key)

    # need to get all the statuses from the replies
    pull_reply_ids = list(reply_convos_dict.keys())
    reply_convos = []
    for i in range(len(pull_reply_ids) // 100 + 1):
        pulled_tweets = api.GetStatuses(status_ids=(pull_reply_ids[i * 100:(i + 1) * 100]),
                                        trim_user=True, include_entities=False, map=True)
        for id in pulled_tweets:
            try:
                status = pulled_tweets.get(id).AsDict()
            except AttributeError:
                print("Problem with status", id, pulled_tweets.get(id, " status not found"))
            reply_convos.append((status[text_key], reply_convos_dict[id]))
            # print("reply convo:", reply_convos[-1])

    with open(f"tweet_files/{twitter_handle}_tweets.txt", 'w') as savefile:
        unicode_errors = 0
        for q, a in quote_convos + reply_convos:
            try:
                savefile.write(q + " +++|+++ \n" + a + " +++$+++ \n")
            except UnicodeEncodeError:
                unicode_errors += 1
                # print("Problem saving tweet, contains weird characters:")
                # print("Tweets: ", q, a)
        print(f"There were {unicode_errors} unicode errors when saving the tweets as '.txt' files.")
    return

interest_list = ["maggieNYT"]


for user in interest_list:
    pull_and_save_tweets(user)
