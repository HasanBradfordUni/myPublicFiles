def create_mealy_machine(input_string, accepted_string):
    if len(input_string) != len(accepted_string):
        raise ValueError("Input and accepted strings must be of equal length")

    states = set()
    alphabet = set(input_string)
    transition_function = {}
    output_function = {}
    initial_state = 'q0'
    
    for i in range(len(input_string)):
        states.add('q' + str(i))
        transition_function['q' + str(i)] = {}
        output_function['q' + str(i)] = {}
        for char in alphabet:
            if input_string[i] == char:
                transition_function['q' + str(i)][char] = 'q' + str(i+1)
                output_function['q' + str(i)][char] = accepted_string[i]
            else:
                transition_function['q' + str(i)][char] = 'q0'
                output_function['q' + str(i)][char] = '-'

    states.add('q' + str(len(input_string)))
    transition_function['q' + str(len(input_string))] = {}
    output_function['q' + str(len(input_string))] = {}
    for char in alphabet:
        transition_function['q' + str(len(input_string))][char] = 'q0'
        output_function['q' + str(len(input_string))][char] = '-'

    return MealyMachine(states, alphabet, transition_function, output_function, initial_state)

def main():
    input_string = input("Enter the input string: ")
    accepted_string = input("Enter the accepted string: ")

    mealy_machine = create_mealy_machine(input_string, accepted_string)

    input_sequence = input("Enter the input sequence: ")

    output_sequence = ''
    for symbol in input_sequence:
        output = mealy_machine.transition(symbol)
        output_sequence += output

    print("Output sequence:", output_sequence)

if __name__ == "__main__":
    main()
