from string import ascii_lowercase, ascii_uppercase
from math import sqrt


def score(energy):
    return 10000 / (energy - 750)


def calculate_energy(a):
    return sum(
        sqrt((a[i][0] - a[i - 1][0]) ** 2 + (a[i][1] - a[i - 1][1]) ** 2)
        for i in range(1, len(a))
    )


def main():
    state = list(input().split())

    new_state = []
    for item in state:
        new_state.append((
            (ascii_lowercase + ascii_uppercase).find(item[0]),
            int(item[1:])
        ))

    energy = calculate_energy(new_state)

    print("Energy: {} Score: {}".format(energy, score(energy)))


if __name__ == "__main__":
    main()
