from termcolor import colored
import time
import sys

def ask_questions(questions_and_actions):
    answers = []
    colored_question_part = colored("Y=Yes", 'green') + " / " + colored("N=No ", 'blue')
    for question_action in questions_and_actions:
        question = question_action['question']
        function = question_action['function']
        message = question_action['message']

        colored_question = '\033[1m' + question + " " + colored_question_part + '\033[0m'
        while True:
            answer = input(colored_question).strip().lower()
            print()  # Adding a line after user input

            if answer in ['y', 'n']:
                answer_boolean = answer == 'y'
                answers.append(answer_boolean)
                if answer_boolean:
                    print(message)
                    function()
                break
            else:
                print(colored('\033[1mInvalid input, please enter "y" or "n".\033[0m', 'red'))
                time.sleep(1)
    return answers

def menu(menu_structure, breadcrumb='', is_root_menu=False):
    while True:
        print()  # Adding a line before breadcrumb
        print(colored(breadcrumb, attrs=['underline']))

        print(colored("Choose an option:", attrs=['bold']))
        for index, option in enumerate(menu_structure):
            message = option['message']
            print(colored(f"{index + 1}: {message}", 'green'))

        if is_root_menu:
            print(colored("E: Exit Application", 'yellow'))  # Yellow Exit option in root menu
            prompt_message = "Press the corresponding number, or E: "
        else:
            print(colored("0: Back to Previous Menu", 'blue'))  # Blue "Back" option in submenus
            print(colored("E: Exit Application", 'yellow'))  # Yellow Exit option in submenus
            prompt_message = "Press the corresponding number, or 0/E: "

        selected_option = input(colored(prompt_message, attrs=['bold']))
        print("-" * 40)  # Adding a line after user input

        if selected_option == 'E':
            sys.exit()  # Exit the application if 'E' is pressed
        if not is_root_menu and selected_option == '0':
            return

        try:
            selected_option = int(selected_option) - 1  # Convert to index
        except ValueError:
            print(colored('\033[1mInvalid option, please try again.\033[0m', 'red'))
            time.sleep(1)
            continue

        if 0 <= selected_option < len(menu_structure):
            option_value = menu_structure[selected_option]
            function = option_value.get('function')
            sub_menu_structure = option_value.get('sub_menu')
            message = option_value['message']
            if function:
                if sub_menu_structure:
                    new_breadcrumb = breadcrumb + ' > ' + message
                    function(sub_menu_structure, breadcrumb=new_breadcrumb)
                else:
                    function()
            else:
                print(colored('\033[1mNo function associated with this option, please try again.\033[0m', 'red'))
                time.sleep(1)
        else:
            print(colored('\033[1mInvalid option, please try again.\033[0m', 'red'))
            time.sleep(1)
