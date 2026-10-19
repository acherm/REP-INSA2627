from jinja2 import Template

# Load the template
template_content = open('property_template.py.jinja').read()
template = Template(template_content)

# Define different variability factors
factors = {
    "operation1": "(x + y) + z",
    "operation2": "x + (y + z)",
    "repetitions": 1000,  # Can be changed to any number of repetitions
}

# Render the template with specific values
generated_code = template.render(factors)

# Save the generated code to a Python file
with open('generated_property_check.py', 'w') as f:
    f.write(generated_code)

print("Generated code has been written to 'generated_property_check.py'.")

factor_combinations = [
    {"operation1": "(x + y) + z", "operation2": "x + (y + z)", "repetitions": 1000},
    {"operation1": "x + y", "operation2": "y + x", "repetitions": 500},
    # Add more combinations as needed
]

for factors in factor_combinations:
    generated_code = template.render(factors)
    with open('generated_property_check.py', 'w') as f:
        f.write(generated_code)

    # Run the generated code automatically (in a real scenario, you'd use subprocess)
    print(f"Running check for factors: {factors}")
    exec(generated_code)  # Use exec to run the code directly
