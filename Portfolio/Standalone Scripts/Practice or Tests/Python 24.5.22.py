def rle(text_string):
    current_token = text_string[0]
    compressed = current_token
    counter = 1
    for i in range (1, len(text_string)):
        next_token = text_string[i]
        if next_token != current_token:
            compressed = compressed + str(counter) + next_token
            counter = 1
        else:
            counter = counter + 1
        current_token = next_token
    compressed = compressed + str(counter)
    return compressed

text_string = input("Enter a text string to compress: ")
compressed = rle(text_string)
print(compressed)
