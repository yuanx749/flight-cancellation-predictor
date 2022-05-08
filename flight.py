"""A module for simulation and prediction of flight cancellation."""

import random


def circuit_breaker(prob2, prob4, n_weeks=15):
    """Generate an array of number by random sampling under the policies.

    Raises:
        ValueError: If probability is negative.

    Returns:
        A list of number where positive number indicates break trigger and
        -1 indicates cancellation.
    """

    prob0 = 1 - prob2 - prob4
    if prob0 < 0:
        raise ValueError("Probability of no break is less than zero.")
    # maxmimum 10-week break
    lst = [0] * (n_weeks + 10)
    i, j = 0, 3
    while i < n_weeks:
        if lst[i] == -1:
            i += 1
            continue
        j = max(j, i + 3)
        weeks = random.choices([0, 2, 4], weights=[prob0, prob2, prob4])[0]
        lst[i] = weeks
        if weeks == 4 and lst[i - 1] == 4 and lst[i - 2] != 2:
            # immediate break
            lst[i + 1 : i + 9] = [-1] * 8
        else:
            lst[j : j + weeks] = [-1] * weeks
            j += weeks
        i += 1
    return lst[:n_weeks]


def predict_prob(prob2, prob4, n_weeks=15, n_simulation=10000):
    """Predict the cancellation probability.

    Args:
        prob2: Probability of small break.
        prob4: Probability of big break.
        n_weeks: Number of weeks.
        n_simulation: Number of simulation.

    Returns:
        A list of estimated probabilities.
    """

    matrix_weeks = [circuit_breaker(prob2, prob4, n_weeks) for _ in range(n_simulation)]
    transpose = list(zip(*matrix_weeks))
    return [lst.count(-1) / len(lst) for lst in transpose]


if __name__ == "__main__":
    for _ in range(10):
        print(circuit_breaker(0.5, 0.2))
    print(predict_prob(0.5, 0.2))
