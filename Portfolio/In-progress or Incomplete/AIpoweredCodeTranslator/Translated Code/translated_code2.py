def is_palindrome(input_string):
	cleaned_string = input_string.lower().replace(' ', '')
	return cleaned_string == cleaned_string[::-1]

def celsius_to_fahrenheit(celsius):
	return (celsius * 9/5) + 32

def find_second_largest(numbers):
	sorted_numbers = sorted(numbers)
	return sorted_numbers[-2]

if __name__ == "__main__":
	# User inputs
	input_string = input('Enter input string: ')
	celsius = int(input('Enter celsius: '))
	numbers = [int(x) for x in input('Enter numbers (comma separated): ').split(',')]

	# Function calls
	print(is_palindrome(input_string))
	print(find_second_largest(numbers))
	print(celsius_to_fahrenheit(celsius))
