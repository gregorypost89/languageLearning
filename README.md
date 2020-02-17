# The Language Learning Application Repository

# Summary

This application facilitates the language learning process by associating a mnemonic in the user's native langauge with a word in the target language.  

# Introduction

# Project Overview

Perhaps the most challenging aspect of learning a new language is trying to memorize thousands of new words that we have never heard before, and associating that with the word in our own language. 

For example, if I told you that ichi means one, ni means two, and san means three in Japanese, its likely that you would forget these translations not too soon after without some form of repetition.  

Traditionally, we could drill this into our head, much like when we learned our multiplication tables and write ichi means one, ichi means one...over and over again.  This gets mundane pretty quickly, and when done over thousands of words, even the most resilient students will give in.

But as we made the comparison to multiplication tables earlier, there is something we can learn as well.  When we look at our multiples of 5, we notice that every number must end in either a 0 or 5, and they in fact alternate where odd number multiples end in 5 and even numbers end in 0.

When we look at multiples of 8, we notice a different pattern where the numbers in the same end position (factors) decrease by a value of 2 until it wraps around again at 0 back to 8.  This same pattern occurs with 9 but with a decrease of 1 each time.

![multTables](https://imgur.com/Ki3Tw1X)

We may unconsciously do something similar when meeting new people.  If we're at a social event with hundreds of people and meet an accountant named Bill, its going to be hard to remember that among countless other people with various careers of their own.  But if we put some pattern into play using that name to make the association, it makes it a lot easier to remember.

Now while accountants have various tasks, lets make the association as simple as possible so that we can remember it.  Something like the following:

![bill](https://imgur.com/9W4eLVf)

If we simply associate just this sentence with the person we met, we accomplish two things.  "He helps people to pay the bills" reminds us that he's an accountant, and "pay the **bills**" reminds us that his name is Bill.

Now taking this all into account, lets go back to our original Japanese example.  To remind ourselves what those words are: ichi means one, ni means two, and san means three in Japanese.  We don't really have the words "ichi", "ni" and "san" used in everyday English, but we can use words that sound *similar* that would have the same effect.  We can say that "ichi" sounds like "itchy", "ni" sounds like "knee", and "san" sounds like "son".  Using those words, lets make some sentences:

![oneTwoThree](https://imgur.com/cXjuxOA)

This will make memorizing these words a lot easier to remember.  Notice how we included both the target language word and the target word in one easy-to-remember sentence so that we can automatically associate those words to each other.  

Over time and with more practice, these sentences should be relied on less to the the point where the user does not even need them anymore, but these associations are extremely helpful tools to get a language learner off the ground, especially in the early phases of learning where memorization is heavily emphasized.

# What's included in this project:

This repository will both contain basic command line interfaces requiring minimal dependencies,
as well as more complex GUIs with more robust features that may necessitate further configuration, such as 
a running Redis server to manage database cache and queue.

# Sentence Generator

This module takes input from the user and generates a sentence based on three inputs:
- The native English spelling
- The target language spelling
- The mnemonic for the target language spelling

## Requirements:

- Python installation
- Command Prompt Terminal

## Necessary Files:

sentenceGenerator.py and the accompanying data folder with .txt files.
All files can be found in the sentenceGenerator directory in this repository.
Make sure that the data folder is in the same directory as sentenceGenerator.py

## Steps:

Navigate to the directory
containing sentenceGenerator.py in your command prompt terminal,
and then run the following command in your console
Make sure that the "data" directory is in the same location as this file.

```
python sentenceGenerator.py
```

You should see the following dialog.  As of now, there is only the "New Entry" option, so press enter to proceed.

![alt text](https://imgur.com/9faEHRm)

We will then be presented with our three input questions.  For this example, 
we will use the english word "cat", the japanese translation "neko", and the mnemonic
for "neko" as "neck":

![alt text](https://imgur.com/8FSEGog)

Once typed in, the program generates the following sentences:

![alt text](https://imgur.com/pyAxWqd)

What this program essentially does under the hood is fetch example sentences from an online 
resource for the english word "baby", and substitutes the mnemonic "action" in those sentences
to generate a new sentence that will help the user associate between
the english word and the word in their target language. 

These examples aren't too great at associating the two words.  But we can select the "Find More Examples"
option to generate more sentences several times until we find something we like.

![alt text](https://imgur.com/rbKRMVa)


# Language Learner

This is the original main program, and utilizes Redis as an in-memory data store to
save user input for word associations.  

## Requirements:

- Python installation
- Command Prompt Terminal

## Source files:

http://www.ashley-bovan.co.uk/words/partsofspeech.html : Parts of speech resource