# Mamoun Mohamed
# 21/11/2024
# Program improved version of the basic calculator.

import os

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference between two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the division of two numbers, handling division by zero."""
    return a / b if b != 0 else "Error: Division by zero."

def power(a, b):
    """Returns the first number raised to the power of the second."""
    return a ** b

def modulus(a, b):
    """Returns the remainder when the first number is divided by the second."""
    return a % b if b != 0 else "Error: Division by zero."

def display_history(history):
    """Displays the history of calculations."""
    if history:
        print("\nCalculation History:")
        for index, record in enumerate(history, 1):
            print(f"{index}. {record}")
    else:
        print("\nNo calculations performed yet.")

def calculator():
    """Runs the improved calculator program."""
    history = []  # List to store past calculations
    operations = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
        "5": ("Exponentiation", power),
        "6": ("Modulus", modulus)
    }

    while True:
        clear_screen()
        print("=== Enhanced Calculator ===")
        print("\nSelect an operation:")
        for key, (name, _) in operations.items():
            print(f"{key}. {name}")
        print("7. View History")
        print("8. Clear History")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        if choice == '9':
            print("Goodbye!")
            break
        elif choice == '7':
            display_history(history)
        elif choice == '8':
            history.clear()
            print("\nHistory cleared.")
        elif choice in operations:
            operation_name, operation_func = operations[choice]

            try:
                num1 = float(input("\nEnter the first number: "))
                num2 = float(input("Enter the second number: "))
                result = operation_func(num1, num2)

                # Log the operation to history
                history.append(f"{operation_name}: {num1} and {num2} => Result: {result}")
                print(f"\n{operation_name} Result: {result}")
            except ValueError:
                print("\nError: Please enter valid numeric values.")
        else:
            print("\nInvalid choice! Please select a valid option.")

        input("\nPress Enter to continue...")

# Run the improved calculator
calculator()
