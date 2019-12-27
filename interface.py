# Source - CITGuru - <script src="https://gist.github.com/CITGuru/01dd41b3367d8bd079e2e538e0c8a396.js"></script>
# Based on source code, put in construction.py
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            '^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$',
            document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


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
                'Help',
                'Exit'
            ],
            'filter': lambda val: val.lower()
        }
    ]

    answers = prompt(questions, style=style)

    if "associate words" in answers.values():
        questions1 = [
            {
                'type': 'confirm',
                'name': 'toBeDelivered',
                'message': 'Is this for delivery?',
                'default': False
            }]

        answers1 = prompt(questions1, style=style)
        print(answers1)

    if "review associations" in answers.values():
        questions2 = [
            {
                'type': 'confirm',
                'name': 'toBeDelivered',
                'message': 'Is this for delivery?',
                'default': False
            }]

        answers2 = prompt(questions2, style=style)
        print(answers2)

    if "add new association" in answers.values():
        questions3 = [
            {
                'type': 'confirm',
                'name': 'toBeDelivered',
                'message': 'Is this for delivery?',
                'default': False
            }]

        answers3 = prompt(questions3, style=style)
        print(answers3)

    if "help" in answers.values():
        print(
            "Associate Words - Provide a word and part of speech for a target word that has no assocation made yet"
            "\n" + "Review Associations - View all words where associations have been made"
            "\n" + "Add New Association - Add a new entry into the database "
            "\n" + "Exit - Terminates the program"
        )

    if "exit" in answers.values():
        print("Terminating program. Thank you for using Language Learning.")
        break

