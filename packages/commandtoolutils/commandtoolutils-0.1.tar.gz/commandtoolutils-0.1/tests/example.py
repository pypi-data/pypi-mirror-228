from menu_utils import menu, ask_questions

def main():
    # Define the menu structure
    menu_structure = [
        {
            'message': 'Say Hello',
            'function': say_hello,
        },
        {
            'message': 'Sub Menu',
            'function': menu,
            'sub_menu': [
                {
                    'message': 'Say Hi',
                    'function': say_hi,
                },
            ],
        },
        {
            'message': 'Ask Questions',
            'function': ask_some_questions,
        }
    ]

    # Display the menu
    menu(menu_structure)

def say_hello():
    print('Hello!')

def say_hi():
    print('Hi!')

def ask_some_questions():
    questions_and_actions = [
        {
            'question': 'Do you like Python?',
            'function': say_yes,
            'message': 'Great! You selected Yes.',
        },
        {
            'question': 'Do you like Java?',
            'function': say_no,
            'message': 'Too bad! You selected No.',
        }
    ]
    ask_questions(questions_and_actions)

def say_yes():
    print('Yes!')

def say_no():
    print('No!')

if __name__ == '__main__':
    main()