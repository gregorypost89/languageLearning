# Goal : We want to have associations with every word in our database
# (redis dependency for database)
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
# Lets start with our dictionary of 20 words
# We use makeJson.py to convert values from our CSV to our JSON file

# Program displays ichi and one. Stores 'number1' as property for template (singular)
# User inputs "itchy" as word link.  Need to store
# User inputs "adjective" as word link type. Need to store
# New store looks like this
# (ichi:one:number1):(itchy:one:adjective)
# Program looks for template based on (number1) and (adjective)
# This (number1) coat is really (adjective)
# Returns:
# This (one) coat is really (itchy)
#
# Part 2:
# Go to next value. The key value store should look like this:
# (ni:two:number)
# Program displays ni and two. Stores 'number' as property for template (plural)
# User inputs "knee" as word link. Need to store
# User inputs "noun" as word link type.  Need to store.
# New store looks like this:
# (ni:two:number):(knee:two:noun)
# Program looks for template based on (number) and (noun)
# These (number) (noun) are very heavy
# Returns:
# These two knee are very heavy
# This doesn't really work.  But lets say we had six (roku) and rock
# These six rock are very heavy
# This works better.  User can modify and save output so it makes sense
# These six rocks are very heavy
# Back to two. We can find a new template:
# We found (number) (noun) on the beach
# We found two knee on the beach
# Still doesn't make sense. But the user can change the input.
# We found two knees on the skeleton
# So the user can be prompted by the output enough to customize and save the
# generated text.


# Use cmd to sketch this out

# import cmd
#
# # Provide a question
#
# question = "ohayou = good morning"
#
#
# class LanguageShell(cmd.Cmd):
#     intro = str(question)
#     prompt = '(input)'
#
#
# if __name__ == '__main__':
#     LanguageShell().cmdloop()

