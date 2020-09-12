from datetime import datetime


class DateProcessor:
    @staticmethod
    def convert_dates(tweet):
        tweet["time"] = datetime.fromisoformat(str(tweet["time"]))
        return tweet

    def process_dates(self, tweet):
        tweet = self.convert_dates(tweet)
        date = tweet["time"].strftime("%Y%m%d")
        hour = tweet["time"].strftime("%H")
        tweet["ymd"] = date
        tweet["hour"] = hour
        return tweet
