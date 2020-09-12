from downloader import S3Downloader
from date_processor import DateProcessor
from tweet_processor import TweetProcessor
from uploader import push_trend_table


def analyse(event, context):
    tweets = S3Downloader().download()
    tweets = map(DateProcessor().process_dates, tweets)
    tweets = TweetProcessor().process(tweets)
    push_trend_table(tweets)
