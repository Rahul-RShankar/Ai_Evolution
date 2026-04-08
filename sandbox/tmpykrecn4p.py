
import sys
import math

def get_number_from_user():
    while True:
        try:
            return float(input("Enter a number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    number = get_number_from_user()
    rows = math.floor(math.log10(number)) + 1
    print("", end="")
    for i in range(rows):
        print("|", end="")
        for j in range(i + 1):
            print(f"({number}) ", end="")
        print("|")
    print("", end="")

if __name__ == "__main__":
    main()
