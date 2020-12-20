from math import sqrt, exp
from random import randint, random
from string import ascii_lowercase, ascii_uppercase


INITIAL_TEMPERATURE = 0.1


# /-----Tools for output-----\

def score(energy):
    return 10000 / (energy - 750)


def generate_answer(state):
    return " ".join(
        (ascii_lowercase + ascii_uppercase)[x] + str(52 - y) for x, y in state
    )

# \-----Tools for output-----/


def calculate_energy(a):
    return sum(
        sqrt((a[i][0] - a[i - 1][0]) ** 2 + (a[i][1] - a[i - 1][1]) ** 2)
        for i in range(1, len(a))
    )


def reverse(state, energy, i, j):

    if i != 0:
        energy -= sqrt(
            (state[i][0] - state[i - 1][0]) ** 2 +
            (state[i][1] - state[i - 1][1]) ** 2
        )
        energy += sqrt(
            (state[j - 1][0] - state[i - 1][0]) ** 2 +
            (state[j - 1][1] - state[i - 1][1]) ** 2
        )

    if j != len(state):
        energy -= sqrt(
            (state[j][0] - state[j - 1][0]) ** 2 +
            (state[j][1] - state[j - 1][1]) ** 2
        )
        energy += sqrt(
            (state[j][0] - state[i][0]) ** 2 +
            (state[j][1] - state[i][1]) ** 2
        )

    state[i:j] = state[i:j][::-1]

    # for k in range((j - i) // 2):
    #     state[i + k], state[j - k - 1] = state[j - k - 1], state[i + k]

    return energy


def generate_state_candidate_reverse_range(state):
    i = randint(0, len(state) - 1)
    j = randint(0, len(state) - 1)

    return min(i, j), max(i, j) + 1


def main():
    with open("input.txt", 'r', encoding="utf-8") as file:
        field = [list(list(map(lambda x: x == '#', line.strip()))) for line in file.readlines()]

    state = [
        (x, y)
        for y in range(len(field))
        for x in range(len(field[0]))
        if field[y][x]
    ]

    temperature = INITIAL_TEMPERATURE

    current_energy = calculate_energy(state)
    print("Initial energy: {} \tInitial score: {}".format(current_energy, round(score(current_energy), 2)))

    step = 1
    while True:
        state_candidate = generate_state_candidate_reverse_range(state)
        candidate_energy = reverse(state, current_energy, *state_candidate)

        if candidate_energy < current_energy:
            current_energy = candidate_energy

        else:
            if random() < exp((current_energy - candidate_energy) / temperature):
                current_energy = candidate_energy
            else:
                reverse(state, candidate_energy, *state_candidate)

        # temperature = INITIAL_TEMPERATURE / step

        if step % 100000 == 0:
            print("Step: {} \tEnergy: {} \tScore: {} \tTemperature: {}".format(
                step, current_energy, round(score(current_energy), 2), temperature
            ))

            with open("output.txt", 'w', encoding="utf-8") as file:
                file.write("Score: " + str(round(score(current_energy), 2)) + "\n" + generate_answer(state))

        step += 1

    print("Result energy: {} \tResult score: {}".format(current_energy, score(current_energy)))


if __name__ == "__main__":
    main()
