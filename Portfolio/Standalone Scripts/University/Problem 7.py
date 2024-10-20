import random

black = 20
white = 16
total = black + white
balls = []

for num in range(black):
    balls.append("Black")
for num in range(white):
    balls.append("White")

while len(balls) > 1:
    index1 = random.randint(0, len(balls)-1)
    ball1 = balls[index1]
    balls.remove(ball1)
    index2 = random.randint(0, len(balls)-1)
    ball2 = balls[index2]
    balls.remove(ball2)

    if ball1 == ball2:
        balls.append("Black")
    else:
        balls.append("White")

print(balls)

