def bi_search(arr: list, x: float | int) -> tuple:
    count = 0
    low = 0
    high = len(arr) - 1
    upper_num = None

    while low <= high:
        count += 1
        mid = (low + high) // 2

        if arr[mid] < x:
            low = mid + 1

        else:
            upper_num = arr[mid]
            high = mid - 1

    return (count, upper_num)


if __name__ == "__main__":
    print(bi_search([1.232, 2.3455, 3.6546674, 4.0, 4.5536225,
          4.5767655, 4.57754757, 5.5355476, 6.5624653, 8.52463452], 4))
