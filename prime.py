def prime_num():
    if a > 0:
        for i in range(2, int(a/2)+1):
            if (a % i)==0:
                print("The number is not prime.")
                break
        else:
            print("The number is prime.")
a=int(input("enter the value of a:"))
prime_num()

