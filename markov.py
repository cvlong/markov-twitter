import os
import sys
from random import choice
import twitter

# https://twitter.com/jane_markov

def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    body = body.rstrip()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    current_key = choice(chains.keys())
    
    while current_key[0][0].istitle() == False:
        current_key = choice(chains.keys())

    text = " ".join(current_key)

    punctuation = ['.', '?', '!']

    while text[-1] not in punctuation and len(text) < 140:
        if current_key in chains:
            string = choice(chains[current_key])
            text = "{} {}".format(text, string)
            current_key = list(current_key[1:])
            current_key.append(string)
            current_key = tuple(current_key)
    
    if len(text) < 140:
        return text
    else:
        make_text(chains)


    # key = choice(chains.keys())
    # words = [key[0], key[1]]
    # while key in chains and len(words) < 140:
    #     # Keep looping until we have a key that isn't in the chains
    #     # (which would mean it was the end of our original text)
    #     #
    #     # Note that for long texts (like a full book), this might mean
    #     # it would run for a very long time.

    #     word = choice(chains[key])
    #     words.append(word)
    #     key = (key[1], word)
    #     # print len(words)
    # 
    # " ".join(words)


def tweet(text):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()

    status = api.PostUpdate(text)
    print status.text



   


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

new_text = make_text(chains)

# Your task is to write a new function tweet, that will take chains as input
tweet(new_text)
