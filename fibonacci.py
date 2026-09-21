def fibonacci(n):
    a=0
    b=1
    print("The fibonacci series is:")
    for i in range(n):
        print(a)
        c=a+b
        a=b
        b=c
n=int(input("enter the number of terms :"))
fibonacci(n)
