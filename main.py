import requests as r
from random import shuffle


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

    category: str = categories[int(input('Choose which category to play (1-10): '))]
    limit: str = input('How many questions would you like to play? (1-25): ')

    url = f'https://the-trivia-api.com/v2/questions?limit={limit}&categories={category}'

    request: r.Response = r.get(url=url)
    return request.json()


def parse_and_play(data):
    total_points: int = 0
    possible_points: int = 0
    difficulty: dict[str: int] = {'easy': 1, 'medium': 2, 'hard': 3}

    for q in data:
        question = q['question']['text']
        answers = q['incorrectAnswers']
        correct_answer = q['correctAnswer']

        answers.append(correct_answer)
        shuffle(answers)

        points = difficulty[q['difficulty']]

        answers_dict: dict[str: str] = {}

        for k, v in enumerate(answers):
            answers_dict[str(k + 1)] = v

        print(question + '\n')

        for k, v in answers_dict.items():
            print(f'{k} - {v}')

        guess: str = input('\nYour guess is(1-4): ').strip()

        if answers_dict[guess] == correct_answer:
            total_points += points
            print(f'\nCorrect for {points} points!')
        else:
            print(f'\nIncorrect, the right answer was {correct_answer}')

        possible_points += points

    if total_points == possible_points:
        print(f'\nPerfect score {str(total_points)} out of {str(possible_points)} possible points!')
    else:
        print(f'\nYou scored a total of {str(total_points)} points out of a possible {str(possible_points)}!')

    play_again: str = input('Would you like to play again?(y/n) ').lower().strip()

    parse_and_play(get_data()) if play_again == 'y' else exit()


if __name__ == '__main__':
    parse_and_play(get_data())
