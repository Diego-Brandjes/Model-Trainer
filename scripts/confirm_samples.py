import math

def main():
# Prompt the user for integer input
    user_input = int(input("CONFIRM SAMPLES: "))

    # Multiply the input by 0.8 and round up the result
    result = math.ceil(user_input * 0.8)

    # Save the result to a file
    file_path = "positive_amount.tmp"
    with open(file_path, "w") as f:
        f.write(str(result))

if __name__ == "__main__":
    main()
