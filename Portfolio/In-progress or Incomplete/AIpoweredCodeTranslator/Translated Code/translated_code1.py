def celsius_to_fahrenheit(celsius):
	return (celsius * 9/5) + 32

def is_palindrome(input_string):
	cleaned_string = input_string.lower().replace(' ', '')
	return cleaned_string == cleaned_string[::-1]

def calculate_average(numbers):
	return sum(numbers) / len(numbers)

if __name__ == "__main__":
	# User inputs
	celsius = int(input('Enter celsius: '))
	input_string = input('Enter input string: ')
	numbers = [int(x) for x in input('Enter numbers (comma separated): ').split(',')]

	# Function calls
	print(celsius_to_fahrenheit(celsius))
	print(calculate_average(numbers))
	print(is_palindrome(input_string))
