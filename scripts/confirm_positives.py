def main():
    user_input = 0
    user_input = input("CONFIRM POSITIVES: ")  # Prompt the user for input
    user_input = user_input * 0.8
    round(user_input)

    file_path = "positive_amount.tmp"
    with open(file_path, "w") as f:
        f.write(user_input)

if __name__ == "__main__":
    main()
