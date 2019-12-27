from __future__ import print_function, unicode_literals
import regex

from lxml import html
import requests

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

import json

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

questions = [
        {
            'type': 'list',
            'name': 'mainMenu',
            'message': 'Please select an option',
            'choices': [
                'New Entry',
            ],
            'filter': lambda val: val.lower()
        }
    ]

answers = prompt(questions, style=style)

answers1, answers2, answers3 = (), (), ()

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

combo = answers3 + answers2
url = 'https://www.merriam-webster.com/dictionary/' + answers1 + '#examples/'
page = requests.get(url)
tree = html.fromstring(page.content)
# This will create a list of sentences:
sentences = tree.xpath('//span[@class="ex-sent  t no-aq sents"]/text()')
wordInSentence = tree.xpath('//em[@class="mw_t_it"]/text()')
cleanedSentences = []
firstPart = []
secondPart = []
for x in sentences:
    x = x.replace('\n', '')
    x = x.strip()
    cleanedSentences.append(x)


for y in cleanedSentences:
    if cleanedSentences.index(y) is 0:
        firstPart.append(y)
    elif cleanedSentences.index(y) % 2 is 0:
        firstPart.append(y)
    else:
        secondPart.append(y)

for z in range(0, len(cleanedSentences) - 1):
    try:
        alpha = (combo + ' ' + str(wordInSentence[z]) + ' ' + cleanedSentences[z + 1])
    except IndexError:
        continue
    if alpha[0].isupper() is True:
        print(alpha)
    beta = (cleanedSentences[z] + ' ' + str(wordInSentence[z]) + ' ' + combo)
    if beta[0].isupper() is True:
        print(beta)