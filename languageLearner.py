from __future__ import print_function, unicode_literals

from lxml import html
import requests

import pprint
from PyInquirer import style_from_dict, Token, prompt

import redis
import json
import sys

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
try:
    with open('data/dataSample.json') as json_file:
        data = json.load(json_file)
except IOError:
    print("dataSample.json not found")
    questionInit = [
        {
            'type': 'confirm',
            'name': 'editPrompt',
            'message': 'Would you like to create a new dataSample.json file?',
            'default': False
        },
    ]
    answerInit = prompt(questionInit, style=style).get(u"editPrompt")
    if answerInit is True:
        newJson = {"1": {"definition": "Ah!", "sentence": "VOID",
                         "definitionPos": "interjection",
                         "phoneticPos": "interjection",
                         "romaji": "ah", "phonetic": "ah"}}
        dfJson = pd.DataFrame(data=newJson)
        dfJson.to_json("data/dataSample.json")
        print("File successfully created.")
        with open('data/dataSample.json') as json_file:
            data = json.load(json_file)
    else:
        print("Please ensure that a dataSample.json file exists in the data"
              "folder to use this program.")
        print("Terminating.")
        sys.exit(1)

# Redis Pipeline Configuration #
# Reset DB Values #
with r.pipeline() as pipe:
    for w_id, word in data.items():
        pipe.hmset(w_id, word)
    pipe.execute()

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
                'Beta1',
                'Help',
                'Exit'
            ],
            'filter': lambda val: val.lower()
        }
    ]

    answers = prompt(questions, style=style)

    if "associate words" in answers.values():
        count = 0
        for x in range(1, len(data)):
            store = r.hget(str(x), "phonetic")
            if store == "value":
                word = r.hget(str(x), "romaji")
                print()
                questions1 = [
                    {
                        'type': 'input',
                        'name': 'association',
                        'message': "Type a word that sounds like " + str(
                            word) + " ",
                    }
                ]
                answers1 = prompt(questions1, style=style).get(u"association")
                print(answers1)
                r.hset(x, "phonetic", str(answers1))
                count += 1
        if count is 0:
            print("There are no words needing associations")

    if "review associations" in answers.values():
        wordsNotDone = []
        for x in range(1, len(data) + 1):
            store = r.hget(str(x), "phonetic")
            if store == "value":
                wordsNotDone.append(r.hget(str(x), "romaji"))
            else:
                print(str(r.hget(str(x), "romaji")) + " sounds like " + str(
                    r.hget(str(x), "phonetic")))
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
                'message': "Input the target language word",
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
                'message': 'What is the part of speech for ' + str(
                    answers4) + ' ?',
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
        sentenceList = []
        pairingList = []
        for x in range(1, len(data)):
            store = r.hget(str(x), "phonetic")
            if store != "value":
                vocabDef = r.hget(str(x), "definition")
                vocabPho = r.hget(str(x), "phonetic")
                vocabRom = r.hget(str(x), "romaji")
                partOfSpeech1 = r.hget(str(x), "definitionPos")
                partOfSpeech2 = r.hget(str(x), "phoneticPos")
                pairingList.append(str(x) + ". definition - " + str(
                    vocabDef) + " | romaji - " + str(
                    vocabRom) + " | phonetic - " + str(vocabPho) + " | ")
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
        index = answersEx1[:1]
        for y in range(1, len(df)):
            sentence1 = df.at[y, 'Pos1']
            sentence2 = df.at[y, 'Pos2']
            if sentence1 == pos1dict[index] and sentence2 == pos2dict[index]:
                part1 = (str(df.at[y, 'Pt1']))
                part2 = (str(df.at[y, 'Pt2']))
                part3 = (str(df.at[y, 'Pt3']))
                wordInsert1 = r.hget(str(index), "definition")
                wordInsert2 = r.hget(str(index), "phonetic")
                try:
                    sentenceList.append(
                        part1 + " " + wordInsert1 + " " + part2 + " " + wordInsert2 + " " + part3)
                except (TypeError, IndexError) as e:
                    print("Skip")
        questionsEx2 = [
            {
                'type': 'list',
                'name': 'sentence',
                'message': 'Select an association',
                'choices': [z for z in sentenceList],
            }
        ]
        try:
            answersEx2 = prompt(questionsEx2, style=style).get(u"sentence")
        except IndexError:
            print("No sentences found")
            continue
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

    if "beta1" in answers.values():
        answers11, answers12, answers13 = (), (), ()
        questions11 = [
            {
                'type': 'input',
                'name': 'word',
                'message': "Type a word: ",
            }
        ]
        answers11 = str(prompt(questions11, style=style).get(u"word"))

        questions12 = [
            {
                'type': 'input',
                'name': 'jword',
                'message': "What is the target language word for " + str(
                    answers11) + " ?",
            }
        ]
        answers12 = "(" + str(
            prompt(questions12, style=style).get(u"jword")) + ")"

        questions13 = [
            {
                'type': 'input',
                'name': 'soundsLike',
                'message': "" + str(answers12) + " sounds like: ",
            }
        ]
        answers13 = str(prompt(questions13, style=style).get(u"soundsLike"))

        combo = answers13 + answers12
        url = 'https://www.merriam-webster.com/dictionary/' + answers11 + '#examples/'
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
                alpha = (combo + ' ' + str(wordInSentence[z]) + ' ' +
                         cleanedSentences[z + 1])
            except (IndexError, UnicodeEncodeError) as e:
                continue
            if alpha[0].isupper() is True:
                print(alpha)
            beta = (cleanedSentences[z] + ' ' + str(
                wordInSentence[z]) + ' ' + combo)
            if beta[0].isupper() is True:
                print(beta)
        print(cleanedSentences)
        if len(cleanedSentences) is 0:
            print("Sorry, no example sentences could be generated.")

    if "help" in answers.values():
        print(
            "Associate Words - Provide a word and part of speech for a target word that has no association made yet"
            "\n" + "Review Associations - View all words where associations have been made"
                   "\n" + "Add New Association - Add a new entry into the database "
                          "\n" + "Exit - Terminates the program"
        )

    if "exit" in answers.values():
        print("Terminating program. Thank you for using the Language Learner.")
        sys.exit(1)
