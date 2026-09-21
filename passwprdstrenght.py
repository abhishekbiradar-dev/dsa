import re  # Used for pattern checking in passwords


# List of commonly used passwords
COMMON_PASSWORDS = {
    "password",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "admin",
    "welcome",
    "letmein",
    "abc123",
    "iloveyou",
    "monkey",
    "password123",
    "admin123",
}


# Common predictable sequences found in weak passwords
SEQUENTIAL_PATTERNS = [
    "123456",
    "234567",
    "345678",
    "456789",
    "abcdef",
    "bcdefg",
    "cdefgh",
    "qwerty",
    "asdfgh",
    "zxcvbn",
]


MAX_SCORE = 10


def get_password():
    """Get a non-empty password from the user."""

    while True:
        password = input("Enter your password: ")

        # Stop asking when the user enters a password
        if password:
            return password

        print("Password cannot be empty. Please try again.\n")


def contains_common_pattern(password):
    """Check whether the password contains a common pattern."""

    # Convert the password to lowercase for case-insensitive checking
    lowered = password.lower()

    # Check if the entire password is commonly used
    if lowered in COMMON_PASSWORDS:
        return True

    # Check if a common password is part of a longer password
    # Example: password123 contains "password"
    for common in COMMON_PASSWORDS:
        if common in lowered:
            return True

    # Check for predictable sequences such as 123456 or qwerty
    for pattern in SEQUENTIAL_PATTERNS:
        if pattern in lowered:
            return True

    return False


def has_repeated_characters(password):
    """Check for three or more repeated characters."""

    # Detect patterns such as aaa, 1111 or $$$$
    return bool(re.search(r"(.)\1\1+", password))


def has_excessive_repetition(password):
    """Check whether the password uses too few unique characters."""

    if not password:
        return False

    # Calculate the ratio of unique characters to total characters
    unique_ratio = len(set(password)) / len(password)

    return unique_ratio < 0.4


def check_character_classes(password):
    """Check which types of characters are used."""

    # Check for uppercase, lowercase, numbers and special characters
    return {
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"[0-9]", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }


def has_sequential_characters(password):
    """Check for ascending or descending character sequences."""

    lowered = password.lower()

    # Check each group of four characters in the password
    for i in range(len(lowered) - 3):

        chunk = lowered[i:i + 4]

        if chunk.isdigit() or chunk.isalpha():

            # Convert characters to numeric values for comparison
            values = [ord(c) for c in chunk]

            # Check for sequences such as 1234 or abcd
            ascending = all(
                values[j] == values[j - 1] + 1
                for j in range(1, 4)
            )

            # Check for sequences such as 4321 or dcba
            descending = all(
                values[j] == values[j - 1] - 1
                for j in range(1, 4)
            )

            if ascending or descending:
                return True

    return False


def analyze(password):
    """Calculate the password score and generate suggestions."""

    score = 0
    suggestions = []

    length = len(password)

    # Give points based on password length
    if length >= 8:
        score += 2
    else:
        suggestions.append("Use at least 8 characters.")

    if length >= 12:
        score += 1

    if length >= 16:
        score += 1

    if length >= 20:
        score += 1

    if 8 <= length < 16:
        suggestions.append("Aim for 16 or more characters.")

    # Check the four main character types
    classes = check_character_classes(password)

    if classes["uppercase"]:
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if classes["lowercase"]:
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if classes["number"]:
        score += 1
    else:
        suggestions.append("Add at least one number.")

    if classes["special"]:
        score += 1
    else:
        suggestions.append("Add at least one special character.")

    # Lower the score if a common password or pattern is detected
    if contains_common_pattern(password):
        suggestions.append(
            "Avoid common passwords or predictable patterns."
        )
        score = min(score, 2)

    # Lower the score if sequential characters are found
    if has_sequential_characters(password):
        suggestions.append(
            "Avoid sequential characters such as 1234 or abcd."
        )
        score = min(score, 5)

    # Lower the score if the same character is repeated too much
    if has_repeated_characters(password):
        suggestions.append(
            "Avoid repeated characters such as aaa or 111."
        )
        score = min(score, 5)

    # Check overall character diversity
    if has_excessive_repetition(password):
        suggestions.append("Use a wider variety of characters.")
        score = min(score, 6)

    # Keep the final score between 0 and 10
    score = max(0, min(score, MAX_SCORE))

    return score, suggestions


def strength_label(score):

    # Convert the numerical score into a readable rating
    if score <= 2:
        return "VERY WEAK"
    elif score <= 4:
        return "WEAK"
    elif score <= 6:
        return "MEDIUM"
    elif score <= 8:
        return "STRONG"
    else:
        return "VERY STRONG"


def strength_bar(score):

    # Create a visual meter based on the score
    filled = "█" * score
    empty = "░" * (MAX_SCORE - score)

    return f"[{filled}{empty}]"


def main():

    print("=" * 55)
    print("          PASSWORD STRENGTH ANALYZER")
    print("=" * 55)

    # Get the password from the user
    password = get_password()

    # Run all security checks and calculate the score
    score, suggestions = analyze(password)

    print("\n" + "-" * 55)

    # Display the password entered by the user
    print("Password Entered :", password)

    # Display the analysis results
    print("Password Length  :", len(password))
    print("Security Rating  :", f"{score} / {MAX_SCORE}")
    print("Strength         :", strength_label(score))
    print("Strength Meter   :", strength_bar(score))

    # Show suggestions if any security issues were found
    if suggestions:

        print("\nSuggestions:")

        for suggestion in suggestions:
            print(" -", suggestion)

    else:

        print("\nExcellent!")
        print("Your password passed all basic security checks.")

    print("-" * 55)
    print("Password analysis completed.")
    print("=" * 55)


# Start the program when this file is executed
if __name__ == "__main__":
    main()