# This is a sample Python script.
from exceptiongroup import catch

from src.app.services.math_service import multiply

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    num1: int = 12 # get_int("Enter a num1 number: ")
    num2: float = 12 # get_float("Enter a num2 number: ")
    calculation = multiply(num1, num2)
    print(calculation)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
