studentnames = ["Rob", "Anna", "Huw", "Emma", "Patrice", "Iqbal"] 
absent = 0
present = 0
for student in range (0, len(studentnames)):
    currentStudent = studentnames[student]
    attendance = input("What is the attendance of "+currentStudent+"? ")
    if attendance == "present":
        present += 1
    elif attendance == "absent":
        absent += 1
print(present,"students are present today and",absent,"students are absent today")
