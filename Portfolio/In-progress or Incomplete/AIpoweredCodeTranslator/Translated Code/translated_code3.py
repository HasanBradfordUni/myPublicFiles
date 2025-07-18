def remove_duplicates(input_list):
	return list(set(input_list))


def calculate_average(numbers):
	return sum(numbers) / len(numbers)

if __name__ == "__main__":
	# User inputs
	input_list = input('Enter input list (comma separated): ').split(',')
	numbers = [int(x) for x in input('Enter numbers (comma separated): ').split(',')]

	# Function calls
	print(remove_duplicates(input_list))
	print(calculate_average(numbers))
