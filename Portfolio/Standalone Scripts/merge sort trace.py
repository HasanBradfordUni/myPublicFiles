def merge_sort_trace(arr):
    trace_table = []

    def merge_sort(arr, depth=0):
        nonlocal trace_table
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        trace_table.append([depth, "Divide", arr[:], left[:], right[:]])

        left = merge_sort(left, depth + 1)
        right = merge_sort(right, depth + 1)

        merged = merge(left, right, depth)

        trace_table.append([depth, "Merge", merged[:], left[:], right[:]])

        return merged

    def merge(left, right, depth):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged

    merge_sort(arr)

    return trace_table

# Example usage:
arr = [38, 27, 43, 3, 9, 82, 10]
arr.sort(reverse=True)
trace_table = merge_sort_trace(arr)

# Display the trace table
# Display the trace table
print("{:<5} {:<10} {:<25} {:<25} {:<25}".format("Depth", "Operation", "Array", "Left", "Right"))
for row in trace_table:
    print("{:<5} {:<10} {:<25} {:<25} {:<25}".format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))

