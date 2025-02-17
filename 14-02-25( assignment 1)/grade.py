# input value
score = int(input("enter your score: "))

# conditions
if(score >= 90 and score <= 100):
    print("grade is A")
elif(score >= 80 and score < 90):
    print("grade is B")
elif(score >= 50 and score < 80):
    print("grade is C")
elif(score >= 35 and score < 50):
    print("grade is D")
else:
    print("you fail...")