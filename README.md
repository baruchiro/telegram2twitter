# telegram2twitter

My custom Telegram Bot to customize messages and tweet them with my Twitter account.

## How to use

### Variables

Set the next variables in the `.env` file. You can insert them with the script CLI if you want.

The next values are available in your [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps):

 - `TELEGRAM_TWITTER_CONSUMER_KEY`
 - `TELEGRAM_TWITTER_CONSUMER_SECRET`
 - `TELEGRAM_TWITTER_ACCESS_TOKEN`
 - `TELEGRAM_TWITTER_TOKEN_SECRET`

You need also to ask Telegram [BotFather](https://t.me/botfather) to give you the *Bot Access Token* for `TELEGRAM_TWITTER_BOT_TOKEN`.

Last variable is your `TELEGRAM_TWITTER_USER_ID`. You can launch the bot without it, and then you can get it by running the command `/id` in the bot.
