import unittest
from timeout_decorator import timeout
from unittest.mock import patch, MagicMock
from commandtoolutils import ask_questions, menu

import functools
def catch_system_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SystemExit:
            pass
    return wrapper

class TestMenuTools(unittest.TestCase):
    
    @timeout(5)
    @patch('builtins.input', return_value='y')
    @catch_system_exit
    def test_ask_questions_yes(self, mock_input):
        def dummy_function():
            pass

        questions_and_actions = [
            {
                'question': 'Do you like Python?',
                'function': dummy_function,
                'message': 'Great! You selected Yes.'
            }
        ]

        answers = ask_questions(questions_and_actions)
        self.assertEqual(answers, [True])

    @timeout(5)
    @patch('builtins.input', return_value='1')
    @catch_system_exit
    def test_menu(self, mock_input):
        dummy_function = MagicMock()

        menu_structure = [
            {
                'message': 'Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)
        
        # Check if the correct function was called
        dummy_function.assert_called_once()

    @timeout(5)
    @patch('builtins.input', return_value='y')
    @catch_system_exit
    def test_ask_questions_yes(self, mock_input):
        dummy_function = MagicMock()

        questions_and_actions = [
            {
                'question': 'Do you like Python?',
                'function': dummy_function,
                'message': 'Great! You selected Yes.'
            }
        ]

        answers = ask_questions(questions_and_actions)
        self.assertEqual(answers, [True])
        
        # Check if the correct function was called
        dummy_function.assert_called_once()

    @timeout(5)
    @patch('builtins.input', side_effect=['1', 'E'])
    @catch_system_exit
    def test_menu_root_menu(self, mock_input):
        def dummy_function():
            pass

        menu_structure = [
            {
                'message': 'Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', side_effect=['1', '0', 'E'])
    @catch_system_exit
    def test_menu_sub_menu(self, mock_input):
        def dummy_function():
            pass

        sub_menu_structure = [
            {
                'message': 'Sub Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Sub Option 2',
                'function': dummy_function,
            }
        ]

        menu_structure = [
            {
                'message': 'Option 1',
                'function': menu,
                'sub_menu': sub_menu_structure
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', side_effect=['3', 'E'])
    @catch_system_exit
    def test_menu_invalid_option(self, mock_input):
        def dummy_function():
            pass

        menu_structure = [
            {
                'message': 'Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', return_value='n')
    @catch_system_exit
    def test_ask_questions_no(self, mock_input):
        def dummy_function():
            pass

        questions_and_actions = [
            {
                'question': 'Do you like Python?',
                'function': dummy_function,
                'message': 'Great! You selected Yes.'
            }
        ]

        answers = ask_questions(questions_and_actions)
        self.assertEqual(answers, [False])

    @timeout(5)
    @patch('builtins.input', side_effect=['1', '0', 'E'])
    @catch_system_exit
    def test_menu_back_to_previous_menu(self, mock_input):
        def dummy_function():
            pass

        sub_menu_structure = [
            {
                'message': 'Sub Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Sub Option 2',
                'function': dummy_function,
            }
        ]

        menu_structure = [
            {
                'message': 'Option 1',
                'function': menu,
                'sub_menu': sub_menu_structure
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', side_effect=['a', 'y'])
    @catch_system_exit
    def test_ask_questions_invalid_input(self, mock_input):
        def dummy_function():
            pass

        questions_and_actions = [
            {
                'question': 'Do you like Python?',
                'function': dummy_function,
                'message': 'Great! You selected Yes.'
            }
        ]

        # Test the ask_questions function
        answers = ask_questions(questions_and_actions)
        
        self.assertEqual(answers, [True])
        self.assertEqual(mock_input.call_count, 2)

    @timeout(5)
    @patch('builtins.input', side_effect=['1', 'E'])
    @catch_system_exit
    def test_menu_empty_menu_structure(self, mock_input):
        menu_structure = []

        # Test the menu function
        with self.assertRaises(ValueError):
            menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', side_effect=['1', 'E'])
    @catch_system_exit
    def test_menu_option_with_no_function(self, mock_input):
        menu_structure = [
            {
                'message': 'Option 1',
            }
        ]

        # Test the menu function
        with self.assertRaises(ValueError):
            menu(menu_structure, is_root_menu=True)

    @timeout(5)
    @patch('builtins.input', side_effect=['1', 'E'])
    @catch_system_exit
    def test_menu(self, mock_input):
        def dummy_function():
            pass

        menu_structure = [
            {
                'message': 'Option 1',
                'function': dummy_function,
            },
            {
                'message': 'Option 2',
                'function': dummy_function,
            }
        ]

        # Test the menu function
        menu(menu_structure, is_root_menu=True)
        
        # Check that the input function was called twice (once for the selection, once for the 'E' to exit)
        self.assertEqual(mock_input.call_count, 2)

    @timeout(5)
    @patch('builtins.input', side_effect=['a', '1', 'E'])
    @catch_system_exit
    def test_menu_invalid_input(self, mock_input):
        menu_structure = [
            {
                'message': 'Option 1',
                'function': lambda: print('Option 1 selected'),
            },
            {
                'message': 'Option 2',
                'function': lambda: print('Option 2 selected'),
            }
        ]

        # Test the menu function
        with self.assertRaises(SystemExit):
            menu(menu_structure, is_root_menu=True)

        self.assertEqual(mock_input.call_count, 3)


if __name__ == '__main__':
    unittest.main()
