from src.app.core.decorators import log_execution_time, print_method_signature
@log_execution_time
@print_method_signature
def multiply(num1: int, num2: float) -> float:
    return num1 * num2
