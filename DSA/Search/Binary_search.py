from icecream import ic

def binary_search(array, target):
    left, right = 0, len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # Target not found


values = [1, 6, 5, 32, 9, 32, 23, 4, 14, 7, 8, 0, 12, 18, 11, 10, 16, 17]
sortedarray = sorted(values)
Target = 12
ic(sortedarray)

index = binary_search(sortedarray, Target)  # Corrected function call
print("Index:", index, "Target:", Target)