def find_second_largest(numbers):
	sorted_numbers = sorted(numbers)
	return sorted_numbers[-2]

def is_palindrome(input_string):
	cleaned_string = input_string.lower().replace(' ', '')
	return cleaned_string == cleaned_string[::-1]

if __name__ == "__main__":
	# User inputs
	numbers = [int(x) for x in input('Enter numbers (comma separated): ').split(',')]
	input_string = input('Enter input string: ')

	# Function calls
	print(find_second_largest(numbers))
	print(is_palindrome(input_string))
