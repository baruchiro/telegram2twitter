import tweepy


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret) -> None:
        # The access tokens can be found on your applications's Details
        # page located at https://dev.twitter.com/apps (located
        # under "Your access token")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

    def status(self, message) -> None:
        # If the application settings are set for "Read and Write" then
        # this line should tweet out the message to your account's
        # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
        self._api.update_status(status=message)
