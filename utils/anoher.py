import math
import timeit


s: str = "ADFS WERGER GNTHFGNMH FGEDRFHGGDFG ASDASD DFS"
max_length = 12


def _spliters():
    ss = s.split(" ")
    ss_length = len(ss)
    pointer = 0
    end_ss = []
    while True:
        if pointer < ss_length - 1:
            if (len(ss[pointer]) + len(ss[pointer + 1])) < max_length:
                end_ss.append(f"{ss[pointer]} {ss[pointer + 1]}")
                pointer += 2
            else:
                end_ss.append(ss[pointer])
                pointer += 1
        else:
            break
    return end_ss


def split_string(s, max_length):
    if len(s) <= max_length:
        return [s]

    if " " not in s:
        raise ValueError(
            "Невозможно разделить строку: отсутствуют пробелы для разбиения."
        )

    space_positions = [i for i, ch in enumerate(s) if ch == " "]

    mid_index = math.ceil(len(space_positions) / 2) - 1  # приводим к 0-индексации
    split_index = space_positions[mid_index]

    left_part = s[:split_index]
    right_part = s[split_index + 1 :]

    return split_string(left_part, max_length) + split_string(right_part, max_length)


def split_string_part():
    if len(s) <= max_length:
        return [s]

    if " " not in s:
        raise ValueError(
            "Невозможно разделить строку: отсутствуют пробелы для разбиения."
        )

    space_positions = [i for i, ch in enumerate(s) if ch == " "]
    mid_index = math.ceil(len(space_positions) / 2) - 1
    split_index = space_positions[mid_index]

    left_part = s[:split_index]
    right_part = s[split_index + 1 :]

    return split_string(left_part, max_length) + split_string(right_part, max_length)


result = timeit.timeit(
    split_string_part,
)
result_my = timeit.timeit(_spliters)
print(result)
print(result_my)
print(split_string_part())
print(_spliters())
