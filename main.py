# This is a sample Python script.
from exceptiongroup import catch


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def multiply(num1: int, num2: float) -> float:
    return num1 * num2

def get_int(message: str) -> int:
    num: int
    while True:
        try:
            num = int(input(message))
            break
        except ValueError:
            print('Please enter an int number.')
    return num

def get_float(message: str) -> float:
    num: float
    while True:
        try:
            num = float(input(message))
            break
        except ValueError:
            print('Please enter a float number.')
    return num

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('-' * 10)
    num1: int = get_int("Enter a num1 number: ")
    num2: float = get_float("Enter a num2 number: ")
    calculation = multiply(num1, num2)
    print(calculation)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
