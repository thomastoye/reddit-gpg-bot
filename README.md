# Reddit GNU Privacy Guard Bot

This a a [reddit](http://www.reddit.com) bot that lives on the [/r/GPGpractice](http://www.reddit.com/r/GPGpractice/) subreddit. Currently, it doesn't do a whole lot, but the plan is to automatically respond to new threads.

## Functionality

### Replying to threads

The bot will periodically scan for new threads on /r/GPGpractice. When it finds one, it will attempt to extract a public key and import it. At the moment, this is effective ~75% of the time. The 25% of threads that didn't make it didn't contain a public key for the most part (questions, accidentally posting a private key, ill-formatted keys, ...).

Currently, the following mechanisms are supported:

* Public key directly in selftext
* A link to [pastebin.com](http://www.pastebin.com)

Unsupported:

* Links to other pastebin services
* Links key servers: `gnupg-python` behaves weirdly when requesting keys from keyservers: the first time, it works, the second time not (even after deleting them from the key ring)
* Only providing a fingerprint

I was surprised to see a few people accidentally posting private keys. Since this is very dangerous behaviour, I decided that the bot will warn in those cases.

### Replying to private messages

When the bot receives a private message, it will assume it's a GPG encrypted message and try to decrypt it. If it's able to decrypt it, it will echo back the decrypted text to confirm. If can't decrypt the message, it sends back that it was unable to decrypt, along with the stderr of the GPG command.

## Development

This project is being developed in Python 3.x. For the exact version, see the `enviroment.txt` file. `virtualenv` is used, and per convention, the dependencies can be found in `requirements.txt`.

## Deployment

This project is deployed on [Heroku](http://www.heroku.com) as a worker. It's deployed on the free tier, so it will only be active 18 hours a day. In the worst case scenario, you might have to wait 6 hours before it replies. I might look into hosting this on my personal server, but it's not a priority at the moment.

## Contributing

Feel free to make a pull request, or to get in touch if you have any questions!

