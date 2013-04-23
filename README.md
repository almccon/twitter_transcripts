twitter_transcripts
===================

Tools for processing twitter transcripts

Workflow:

For each transcript: 

cat tweets_2013-01-01.html | ./process_hootsuite.py > clean_tweets_reversed_2013-01-01.html

Then, for all transcripts:

./tweet_stats.py clean_tweets_reversed_*.html | ./user_stats.py > output.tsv

Detailed steps:

1) Copy html source of tweets from HootSuite Dashboard. 

2) Feed this html into process_hootsuite.py, which cleans up the HTML and reverses the chronological order.

3) Feed all of the cleaned-up html files into tweet_stats.py (which extracts username, date, and timestamp for each tweet)

4) Pipe the output of tweet_stats.py into user_stats.py (which counts number of tweets for each date and user and outputs tsv)

5) Generate charts using transcript_charts.R and the tsv output of user_stats.py
