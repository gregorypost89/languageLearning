from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from bs4 import BeautifulSoup

import requests
import urllib
import sys

style = style_from_dict({
    Token.QuestionMark: '#FF5100  bold',  #E91E63 default
    Token.Selected: '#FF5100 bold', #673AB7 default
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

cleanedsentences = []

def mainfunction(site):
    html = urllib.urlopen(site).read()
    soup = BeautifulSoup(html, "lxml")
    page = requests.get(site)
    divs = soup.findAll('div', {"class": "text", "dir": "ltr", "flex": ""})
    for i in divs:
        i = i.get_text().replace('\n', '').strip()
        cleanedsentences.append(i)
    results = []
    counter = 0

    for x in range(1, 20):
        try:
            queue = cleanedsentences[x].split()
        except IndexError:
            print("Sorry, no results found.")
            questionretry = [
                {
                    'type': 'confirm',
                    'name': 'editPrompt',
                    'message': 'Would you like to try again?',
                    'default': False
                },
            ]
            answerretry = prompt(questionretry, style=style).get(u"editPrompt")
            if answerretry is False:
                print("Terminating program. Thank you for using the Sentence Generator.")
                sys.exit(1)
            else:
                break
        for y in range(0, len(queue)):
            if answers3pos == "noun":
                if queue[y].lower() in nouns:
                    queue[y] = answers3
                    n = ' '.join(queue)
                    if n not in results:
                        results.append(n)
                    counter += 1
            elif answers3pos == "verb":
                if queue[y].lower() in verbs:
                    queue[y] = answers3
                    n = ' '.join(queue)
                    if n not in results:
                        results.append(n)
                    counter += 1
            elif answers3pos == "adjective":
                if queue[y].lower() in adjectives:
                    queue[y] = answers3
                    n = ' '.join(queue)
                    if n not in results:
                        results.append(n)
                    counter += 1
            elif answers3pos == "adverb":
                if queue[y].lower() in adverbs:
                    queue[y] = answers3
                    n = ' '.join(queue)
                    if n not in results:
                        results.append(n)
                    counter += 1

    for item in results:
        print(item)

    if counter == 0:
        print("Sorry, no results found.")

    del cleanedsentences[:]

# Database imports


with open('data/nouns.txt', 'r') as f:
    nouns = [line.strip() for line in f]

with open('data/verbs.txt', 'r') as f:
    verbs = [line.strip() for line in f]

with open('data/adjectives.txt', 'r') as f:
    adjectives = [line.strip() for line in f]

with open('data/adverbs.txt', 'r') as f:
    adverbs = [line.strip() for line in f]

answers1, answers2, answers3 = (), (), ()
answers3pos = ""

while True:
    questions = [
            {
                'type': 'list',
                'name': 'mainMenu',
                'message': 'Please select an option',
                'choices': [
                    'New Entry',
                    'Exit'
                ],
                'filter': lambda val: val.lower()
            }
        ]

    answers = prompt(questions, style=style)

    if "new entry" in answers.values():
        questions1 = [
                {
                    'type': 'input',
                    'name': 'word',
                    'message': "Type a word: ",
                }
            ]
        answers1 = str(prompt(questions1, style=style).get(u"word"))

        questions2 = [
            {
                'type': 'input',
                'name': 'jword',
                'message': "What is the target language word for " + str(answers1) + " ?",
            }
        ]
        answers2 = "(" + str(prompt(questions2, style=style).get(u"jword")) + ")"

        questions3 = [
            {
                'type': 'input',
                'name': 'soundsLike',
                'message': "" + str(answers2) + " sounds like: ",
            }
        ]
        answers3 = str(prompt(questions3, style=style).get(u"soundsLike"))

        if answers3 in nouns:
            answers3pos = "noun"
        elif answers3 in verbs:
            answers3pos = "verb"
        elif answers3 in adjectives:
            answers3pos = "adjective"
        elif answers3 in adverbs:
            answers3pos = "adverb"

        combo = answers3 + " (" + answers2 + ") "
        page = 1
        url = 'https://tatoeba.org/eng/sentences/search?from=und&to=und&query=' + answers1 + '&from=eng&to=eng&page=' + str(page)
        mainfunction(site=url)

        while True:
            questionNext = [
                {
                    'type': 'list',
                    'name': 'mainMenu',
                    'message': 'Please select an option',
                    'choices': [
                        'See more examples',
                        'Return to main menu',
                        'Exit'
                    ],
                    'filter': lambda val: val.lower()
                }
            ]

            answerNext = prompt(questionNext, style=style)

            if "see more examples" in answerNext.values():
                page += 1
                url = 'https://tatoeba.org/eng/sentences/search?from=und&to=und&query=' + answers1 + '&from=eng&to=eng&page=' + str(page)
                mainfunction(site=url)

            elif "return to main menu" in answerNext.values():
                break

            elif "exit" in answerNext.values():
                print("Terminating program. Thank you for using the Sentence Generator.")
                sys.exit(1)

    if "exit" in answers.values():
        print("Terminating program. Thank you for using the Sentence Generator.")
        sys.exit(1)