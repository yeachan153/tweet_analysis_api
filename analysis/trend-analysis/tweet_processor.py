import pandas as pd


class TweetProcessor:
    def process(self, tweets):
        processed = []
        tweets = pd.DataFrame(tweets)
        for idx, group in tweets.groupby("ymd"):
            processed += self._get_hourly_max(group)
        return processed

    def _get_hourly_max(self, daily_tweets):
        daily_tweets = daily_tweets[
            daily_tweets["retweets"]
            == daily_tweets.groupby(["hour"])["retweets"].transform("max")
        ].copy()
        daily_tweets.drop("time", axis=1, inplace=True)
        return daily_tweets.to_dict(orient="records")
