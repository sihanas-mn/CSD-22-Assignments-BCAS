a=input("enter a: ")
b=input("enter b: ")
c=input("enter c: ")

if (a==b and b==c):
    print("its a equilateral triangle")
elif(a==b or a==c or b==c):
    print("its a isosceles triangle")
else:
    print("its a scalane triangle")