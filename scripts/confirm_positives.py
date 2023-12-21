def main():
    user_input = input("CONFIRM POSITIVES: ")  # Prompt the user for input
    file_path = "positive_amount.tmp"
    with open(file_path, "w") as f:
        f.write(user_input)

if __name__ == "__main__":
    main()
