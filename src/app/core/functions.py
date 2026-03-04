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
