# password_strength_wordlist.py

from zxcvbn import zxcvbn
from itertools import permutations
import re

def leetspeak(word):
    return word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')

def get_password_strength(password):
    result = zxcvbn(password)
    print("\n🔒 Password Strength Analysis")
    print("----------------------------")
    print("Password:", password)
    print("Score (0–4):", result['score'])
    print("Estimated Crack Time:", result['crack_times_display']['offline_slow_hashing_1e4_per_second'])
    print()

def generate_wordlist(user_inputs):
    words = [v for v in user_inputs.values()]
    variations = []

    # base word variations
    for word in words:
        variations.extend([
            word.lower(), word.upper(), word.capitalize(),
            word + "123", word + "@2024", word[::-1],
            leetspeak(word)
        ])

    # combine words
    for i in range(2, len(words)+1):
        for combo in permutations(words, i):
            variations.append("".join(combo))
            variations.append("".join([leetspeak(w) for w in combo]))

    # add years
    years = [str(y) for y in range(2000, 2026)]
    extended = []
    for word in variations:
        for year in years:
            extended.append(word + year)
    variations.extend(extended)

    # remove duplicates and non-alphanumeric
    final_wordlist = list(set(filter(lambda w: re.match(r'^[a-zA-Z0-9@$.]+$', w), variations)))

    with open("enhanced_wordlist.txt", "w") as f:
        for item in final_wordlist:
            f.write(item + "\n")

    print(f"✅ Wordlist generated: {len(final_wordlist)} entries saved to enhanced_wordlist.txt")

def main():
    print("🔐 Password Strength Analyzer + Wordlist Generator")
    print("--------------------------------------------------")
    password = input("Enter a password to analyze: ")
    get_password_strength(password)

    print("\n🧠 Enter personal info to generate wordlist")
    name = input("Name: ")
    dob = input("Date of Birth (YYYY): ")
    pet = input("Pet’s Name: ")

    user_inputs = {"name": name, "dob": dob, "pet": pet}
    generate_wordlist(user_inputs)


if __name__ == "__main__":
    main()
