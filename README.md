# Reddit GNU Privacy Guard Bot

This a a [reddit](http://www.reddit.com) bot that lives on the [/r/GPGpractice](http://www.reddit.com/r/GPGpractice/) subreddit. Currently, it doesn't do a whole lot, but the plan is to automatically respond to new threads. Note that **the private key of the bot is in this repository**, this is not a mistake, it was done on purpose to help people debug, etc.

## Parsing keys

The bot will periodically scan for new threads. When it finds one, it will attempt to extract a public key and import it. At the moment, this is effective ~75% of the time. The 25% of threads that didn't make it didn't contain a public key for the most part (questions, accidentally posting a private key, ill-formatted keys, ...).

Currently, the following mechanisms are supported:

* Public key directly in selftext
* A link to [pastebin.com](http://www.pastebin.com)
* --A link to the MIT key server-- gnupg-python has weird behaviour when importing from keyservers, sometimes it works, sometimes it doesn't... Not supported until I find the time to investigate (probably never, since only a few people post links like this).

Unsupported:

* Links to other pastebin services
* Links to other key servers
* Only providing a fingerprint

## Replying to threads

The bot will respond to threads with a message, encrypted with the public key of the thread starter.

## Private key warner

I was surprised to see a few people accidentally posting private keys. Since this is very dangerous behaviour, I decided that the bot will warn in those cases.

## python-gnupg

Here are some notes on the `gnupg` module:

### Generate a key

    >>> import gnupg
    >>> gpg = gnupg.GPG(homedir='gpg-homedir')
    >>> bot_gpg_settings = { 'name_real': 'Reddit GPG Bot', 'name_email': '', 'key_type': 'RSA', 'key_length': 4096, 'key_usage': 'ESCA'}
    >>> key_input = gpg.gen_key_input(**bot_gpg_settings)
    >>> bot_key = gpg.gen_key(key_input) # may take a while
    >>> print(bot_key.fingerprint)

### Getting a key from a keyserver

`python-gnupg` is really picky when it comes to the format. These work, sometimes (they tend to time out on my machine if used more than once):

    >>> key = gpg.recv_keys('hkp://pgp.mit.edu', '946563E8A1D683E4')
    >>> key = gpg.recv_keys('hkp://pgp.mit.edu', 'A1D683E4')

## Development

This project is being developed in Python 3.x. For the exact version, see the `enviroment.txt` file. `virtualenv` is used, and per convention, the dependencies can be found in `requirements.txt`.

## Deployment

This project is deployed on [Heroku](http://www.heroku.com) as a worker. It's deployed on the free tier, so it will only be active 18 hours a day. In the worst case scenario, you might have to wait 6 hours before it replies. I might look into hosting this on my personal server, but it's not a priority at the moment.

## Contributing

Feel free to make a pull request, or to get in touch if you have any questions!

