def factorial(n):
    if(n == 0):
        result = 1
        return result
    return n*factorial(n-1)

print("The factorial of:")
inp=int(input())
print("Is:",factorial(inp))

