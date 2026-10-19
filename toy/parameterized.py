import random

def check_property(operation1, operation2, repetitions):
    correct_count = 0
    for _ in range(repetitions):
        x = random.random()
        y = random.random()
        z = random.random()

        # Dynamically evaluate the operations
        result1 = eval(operation1)
        result2 = eval(operation2)

        if result1 == result2:
            correct_count += 1

    print(f"Out of {repetitions} trials, {correct_count} times the property held for {operation1} and {operation2}.")

# Define possible combinations of operations and repetition counts
operations = [
    {"operation1": "(x + y) + z", "operation2": "x + (y + z)"},  # Associativity
    {"operation1": "x + y", "operation2": "y + x"},              # Commutativity
    {"operation1": "(x * y) * z", "operation2": "x * (y * z)"},  # Associativity (multiplication)
    {"operation1": "x * (y / z)", "operation2": "(x * y) / z"}   # Combination of operations
]

# Define different repetition counts
repetitions_list = [500, 1000, 2000]

# Loop through all combinations of operations and repetitions
for op in operations:
    for reps in repetitions_list:
        print(f"\nChecking {op['operation1']} vs {op['operation2']} with {reps} repetitions:")
        check_property(op['operation1'], op['operation2'], reps)
