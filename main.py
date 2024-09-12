from dataclasses import dataclass

import requests as r
from random import shuffle
from colorama import Fore
import time


class Color:
    @staticmethod
    def print_green(string):
        print(Fore.GREEN + string + Fore.RESET)

    @staticmethod
    def print_cyan(string):
        print(Fore.CYAN + string + Fore.RESET)

    @staticmethod
    def print_yellow(string):
        print(Fore.YELLOW + string + Fore.RESET)


@dataclass
class Question:
    question: str = None
    answers: dict[int: str] = None
    correct_answer: str = None
    points: int = None
    
def parse_input(prompt: str, lower: int, upper: int) -> int :
    while True:
        user_input = input(f'\n{prompt}')
        if user_input.isdecimal() and int(user_input) in list(range(lower, upper + 1)):
            return int(user_input)
        else:
            print('Please enter a valid choice.')
            continue
            


def get_data():
    categories: dict[int: str] = {
        1: 'music',
        2: 'sport_and_leisure',
        3: 'film_and_tv',
        4: 'arts_and_literature',
        5: 'history',
        6: 'society_and_culture',
        7: 'science',
        8: 'geography',
        9: 'food_and_drink',
        10: 'general_knowledge'}

    for k, v in categories.items():
        print(f'{k}. {v.replace('_', ' ').title()}')

    category: str = categories[parse_input('\nChoose which category to play (1-10): ', 1, 10)]
    limit: str = parse_input('How many questions would you like to play? (1-20): ', 1, 20)

    url = f'https://the-trivia-api.com/v2/questions?limit={limit}&categories={category}'

    request: r.Response = r.get(url=url)
    return request.json()


def parse_data(data, questions: list[Question]):
    difficulty: dict[str: int] = {'easy': 1, 'medium': 2, 'hard': 3}

    for q in data:
        question: Question = Question()
        question.question = q['question']['text']
        question.correct_answer = q['correctAnswer']

        answers: list[str] = q['incorrectAnswers']
        answers.append(q['correctAnswer'])
        shuffle(answers)

        question.answers = {k: v for k, v in enumerate(answers, start=1)}
        question.points = difficulty[q['difficulty']]

        questions.append(question)


def play_quiz(questions: list[Question]):
    total_points: int = 0
    possible_points: int = 0

    for q in questions:
        print(q.question + '\n')

        for k, v in q.answers.items():
            print(f'{k} - {v}')

        guess: int = parse_input('Enter your guess (1-4):', 1, 4)

        if q.answers[guess] == q.correct_answer:
            total_points += q.points
            Color.print_cyan(f'\nCorrect for {q.points} points!\n')
        else:
            Color.print_yellow(f'\nIncorrect, the right answer was {q.correct_answer}\n')

        possible_points += q.points
        time.sleep(1)

    if total_points == possible_points:
        Color.print_green(f'Perfect score {str(total_points)} out of {str(possible_points)} points!\n')
    else:
        Color.print_green(f'You scored a total of {str(total_points)} out of {str(possible_points)} points!\n')

    play_again: str = input('Would you like to play again?(y/n) ').lower().strip()

    if play_again[0] == 'y':
        questions.clear()
        parse_data(get_data(), questions)
        play_quiz(questions)
    else:
        print('See you next time!')
        exit()


if __name__ == '__main__':
    questions_list: list[Question] = []

    parse_data(get_data(), questions_list)
    play_quiz(questions_list)
