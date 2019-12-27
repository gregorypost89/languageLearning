from __future__ import print_function, unicode_literals
import regex

import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

import redis
import cmd
import json

import pandas as pd

df = pd.read_csv("data/exampleSentences.csv")

# PyInquirer Styles #
style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

# Redis Configuration #

r = redis.Redis(host='localhost', port=6379, db=1)

# Pretty Print Configuration #
pp = pprint.PrettyPrinter(indent=4)

# Loading Json File #
with open('data/dataSample.json') as json_file:
    data = json.load(json_file)

# Redis Pipeline Configuration #
# Reset DB Values #
# with r.pipeline() as pipe:
#     for w_id, word in data.items():
#         pipe.hmset(w_id, word)
#     pipe.execute()

#print(data)

#print(len(data))
#for x in range(0, len(data)):
#    pp.pprint(r.hget(str(x), "definition"))


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

sentenceList = []
pairingList = []
indexValue = 1
partOfSpeech1 = []
partOfSpeech2 = []
pos1dict = {}
pos2dict = {}


def dictmap(n, m):
    return {n: m}


print('Hi, welcome to the Language Translator')

while True:
    print('Main Menu')

    questions = [
        {
            'type': 'list',
            'name': 'mainMenu',
            'message': 'Please select an option',
            'choices': [
                'Associate Words',
                'Review Associations',
                'Add New Association',
                'Make Example Sentences',
                'Help',
                'Exit'
            ],
            'filter': lambda val: val.lower()
        }
    ]

    answers = prompt(questions, style=style)

    if "associate words" in answers.values():
        for x in range(1, len(data)):
            store = r.hget(str(x), "phonetic")
            if store == "value":
                word = r.hget(str(x), "romaji")
                print()
                questions1 = [
                    {
                        'type': 'input',
                        'name': 'association',
                        'message': "Type a word that sounds like " + str(word) + " ",
                    }
                ]
                answers1 = prompt(questions1, style=style).get(u"association")
                print(answers1)
                r.hset(x, "phonetic", str(answers1))

    if "review associations" in answers.values():
        wordsNotDone = []
        for x in range(1, len(data) + 1):
            store = r.hget(str(x), "phonetic")
            if store == "value":
                wordsNotDone.append(r.hget(str(x), "romaji"))
            else:
                print(str(r.hget(str(x), "romaji")) + " sounds like " + str(r.hget(str(x), "phonetic")))
                print(str(r.hget(str(x), "sentence")))
        if len(wordsNotDone) > 0:
            print("Words yet to be translated:")
            pp.pprint(wordsNotDone)

    if "add new association" in answers.values():
        newEntry = str(len(data) + 1)
        questions3 = [
            {
                'type': 'input',
                'name': 'romaji',
                'message': "Input the english spelling for the word",
            }
        ]
        answers3 = prompt(questions3, style=style).get(u"romaji")
        print(answers3)
        r.hset(newEntry, "romaji", str(answers3))

        questions4 = [
            {
                'type': 'input',
                'name': 'definition',
                'message': "Input the definition for the word",
            }
        ]
        answers4 = prompt(questions4, style=style).get(u"definition")
        print(answers4)
        r.hset(newEntry, u"definition", str(answers4))

        questions5 = [
            {
                'type': 'list',
                'name': 'partOfSpeech',
                'message': 'What is the part of speech for ' + str(answers4) + ' ?',
                'choices': [
                    'Noun',
                    'Verb',
                    'Adjective',
                    'Adverb',
                    'Preposition',
                    'Interjection',
                    'Conjunction',
                ],
                'filter': lambda val: val.lower()
            }
            ]
        answers5 = prompt(questions5, style=style).get(u"partOfSpeech")
        print(answers5)
        r.hset(newEntry, "partOfSpeech", str(answers5))

        questions6 = [
            {
                'type': 'input',
                'name': 'phonetic',
                'message': str(answers3) + " sounds like:",
            }
        ]
        answers6 = prompt(questions6, style=style).get(u"phonetic")
        print(answers6)
        r.hset(newEntry, "phonetic", str(answers6))

        questions7 = [
            {
                'type': 'list',
                'name': 'phoneticPos',
                'message': 'What is the part of speech for ' + str(
                    answers6) + ' ?',
                'choices': [
                    'Noun',
                    'Verb',
                    'Adjective',
                    'Adverb',
                    'Preposition',
                    'Interjection',
                    'Conjunction',
                ],
            }
        ]
        answers7 = prompt(questions7, style=style).get(u"phoneticPos")
        print(answers7)
        r.hset(newEntry, "phoneticPos", str(answers7))

        data[newEntry] = r.hgetall(newEntry)
        print("Successfully added to dictionary.")
        with open('data/dataSample.json', 'w') as f:
            json.dump(data, f)

    if "make example sentences" in answers.values():
        del sentenceList[:]
        for x in range(1, len(data)):
            store = r.hget(str(x), "phonetic")
            if store != "value":
                vocabDef = r.hget(str(x), "definition")
                vocabPho = r.hget(str(x), "phonetic")
                vocabRom = r.hget(str(x), "romaji")
                partOfSpeech1 = r.hget(str(x), "definitionPos")
                partOfSpeech2 = r.hget(str(x), "phoneticPos")
                pairingList.append(str(x) + ". definition - " + str(vocabDef) + " | romaji - " + str(vocabRom) + " | phonetic - " + str(vocabPho) + " | ")
                pos1dict.update(dictmap(str(x), str(partOfSpeech1)))
                pos2dict.update(dictmap(str(x), str(partOfSpeech2)))

        questionsEx1 = [
            {
                'type': 'list',
                'name': 'sentence',
                'message': 'Select an association',
                'choices': [y for y in pairingList],
            }
        ]
        answersEx1 = prompt(questionsEx1, style=style).get(u"sentence")
        print(answersEx1)
        index = answersEx1[:1]
        print(pos1dict)
        print(pos2dict)
        for y in range(1, len(df)):
            sentence1 = df.at[y, 'Pos1']
            sentence2 = df.at[y, 'Pos2']
            print(sentence1)
            print(pos1dict[index])
            print(sentence2)
            print(pos2dict[index])
            if sentence1 == pos1dict[index] and sentence2 == pos2dict[index]:
                part1 = (str(df.at[y, 'Pt1']))
                part2 = (str(df.at[y, 'Pt2']))
                part3 = (str(df.at[y, 'Pt3']))
                wordInsert1 = r.hget(str(index), "definition")
                wordInsert2 = r.hget(str(index), "phonetic")
                try:
                    sentenceList.append(part1 + " " + wordInsert1 + " " + part2 + " " + wordInsert2 + " " + part3)
                except TypeError:
                    print("Skip")
            print(sentenceList)
        questionsEx2 = [
            {
                'type': 'list',
                'name': 'sentence',
                'message': 'Select an association',
                'choices': [z for z in sentenceList],
            }
        ]
        answersEx2 = prompt(questionsEx2, style=style).get(u"sentence")
        questionsEx3 = [
            {
                'type': 'confirm',
                'name': 'editPrompt',
                'message': 'Would you like to edit this response?',
                'default': False
            },
        ]
        answersEx3 = prompt(questionsEx3, style=style).get(u"editPrompt")
        print(answersEx3)
        if answersEx3 is True:
            questionsEx4 = [
                {
                    'type': 'input',
                    'name': 'edit',
                    'message': 'Edit the text, and hit enter to save.',
                }
            ]
            answersEx4 = prompt(questionsEx4, style=style).get(u"edit")
            r.hset(str(index), "sentence", str(answersEx4))
        else:
            r.hset(str(index), "sentence", str(answersEx2))
        # if len(sentenceList) == 0:
        #     print("No example sentences found")
        # else:
        #     questionsEx = [
        #         {
        #             'type': 'list',
        #             'name': 'sentence',
        #             'message': 'Select the best available association',
        #             'choices': [y for y in sentenceList],
        #         }
        #         ]
        #     answersEx = prompt(questionsEx, style=style).get(u"sentence")

    if "help" in answers.values():
        print(
            "Associate Words - Provide a word and part of speech for a target word that has no association made yet"
            "\n" + "Review Associations - View all words where associations have been made"
            "\n" + "Add New Association - Add a new entry into the database "
            "\n" + "Exit - Terminates the program"
        )

    if "exit" in answers.values():
        print("Terminating program. Thank you for using Language Learning.")
        break
