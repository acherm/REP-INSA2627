import random
import argparse

def check_property(operation1, operation2, repetitions):
    correct_count = 0
    for _ in range(repetitions):
        x = random.random()
        y = random.random()
        z = random.random()

        # Dynamically evaluate operations
        result1 = eval(operation1)
        result2 = eval(operation2)

        if result1 == result2:
            correct_count += 1

    print(f"Out of {repetitions} trials, the property held {correct_count} times.")

if __name__ == "__main__":
    # Parse arguments at runtime
    parser = argparse.ArgumentParser(description="Check arithmetic property.")
    parser.add_argument('--operation1', type=str, required=True, help="First operation to compare (e.g., '(x + y) + z').")
    parser.add_argument('--operation2', type=str, required=True, help="Second operation to compare (e.g., 'x + (y + z)').")
    parser.add_argument('--repetitions', type=int, required=True, help="Number of repetitions for the check.")

    args = parser.parse_args()

    # Run the property check with runtime arguments
    check_property(args.operation1, args.operation2, args.repetitions)
