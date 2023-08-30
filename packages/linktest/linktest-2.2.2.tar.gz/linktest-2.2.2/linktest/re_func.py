"""
This module is called by auto_generate_testcase_list_from_csv.py:
  1. check_python_method_for_linktest
  2. check_is_valid_ui_format

@author: Wang Lin
"""

import re


def check_python_method_for_linktest(method_string):
    # Regular expression matching rules:
    # 1. The string begins with `def` followed by a space.
    # 2. Then comes a valid Python method name, starting with a letter or underscore, followed by any number of letters, numbers, or underscores.
    # 3. Then comes zero or more spaces, followed by a left parenthesis.
    # 4. Then comes zero or more spaces, followed by `self`, then a comma and at least one character (representing at least one argument).
    # 5. Then any number of characters (including zero), followed by a right parenthesis.
    # 6. Finally, zero or more spaces, followed by a colon.

    pattern = r'^def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*self\s*,.+?\):.*$'
    match = re.match(pattern, method_string)
    return match is not None


def check_is_valid_ui_format(s):
    # Regular expression to match 4 spaces and 'self.browser.' at the start of the string
    pattern = r'^ {4}self\.browser\.'
    if re.match(pattern, s):
        return True
    return False


if __name__ == "__main__":
    # test check_python_method_for_linktest
    method_string = 'def    login (self ,      u):'
    result = check_python_method_for_linktest(method_string)
    print(f'The method string is valid: {result}')

    # test check_is_valid_ui_format
    print("------")
    print(check_is_valid_ui_format('    self.browser.get("https://www.google.com")'))  # return True
    print(check_is_valid_ui_format('    self. browser.get("https://www.google.com")'))  # return False
    print(check_is_valid_ui_format('self.browser.get("https://www.google.com")'))  # return False
    print(check_is_valid_ui_format('     self.browser.get("https://www.google.com")'))  # return False
