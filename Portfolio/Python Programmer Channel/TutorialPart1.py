"""This tutorial will show a lot of basic input/output functions and methods so that
you can start your python programming journey. It wil focus on efficiency and won't
be too complex, there will be more advanced tutorials on my channel in future, so be
sure to like and subscribe."""

#The first in-built function you need to know is print
#print("Hello world")
"""This will allow you to display a piece of text of your choosing to the screen,
in this app it will display to the window on the right -->"""

#Now I will run the program

#So now let's do something a bit more advanced

#let's say we want to store something in memory then print it

#We use a variable, you can name it whatever you want, but it should be descriptive

name = "John"
"""That is one example of a variable, now we can use it to print the name of someone,
however, it doesn't need to be the only thing in the print statement, you can use a comma,
to seperate the name and any text you want to put in as well

print("My name is:",name)

#Okay, so we printed out some text, we can also print out numbers

age = 7

#Now let's try to print this age directly

print("My age is:",age)

#However, what if we want to add 2 numbers and print the result

num1 = 23
num2 = 5

print(num1+num2)

#This time the numbers will be in quotes

num3 = "3"
num4 = "5"

#Write in the comments what you think will happen

#Anyways, let's print out the 2 numbers
print(num3+num4)

#We can use another function 'int' to convert them to numbers
print(int(num3)+int(num4))

#So that was output, what about input, when we want to enter a value

#There is another function for this, 'input'

text = input("Enter something: ")
print("you entered:",text)"""

#We can also put some text inside the input function

"""There are also other ways of inputting text and you can input mnore than just text,
however that is more advanced and requires more tools, we will explore them in
future tutorials, anyways let's try to input a number"""

#num = int(input("Enter a number: ")) #We can use int to convert them to numbers
#otherNum = int(input("Enter another number: "))
#print("The sum of the numbers is:",(num+otherNum))

"""However, a comma is usually better as it automatically adds a space between text in
quotation marks and a variable"""

"""Now we can put everything together to make something"""

name = input("Enter your name: ")
age = int(input("Enter your age: "))
anotherAge = int(input("Enter someone else's age: "))

print("Your details are:\nYour name is:",name,"\nYour age is:",age,
      "\nYou are",(age-anotherAge),"years older than this other person")












