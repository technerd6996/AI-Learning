"""def get_even (numbers):
    even_numbers=[]
    for number in numbers:
        if number % 2 ==0:
            even_numbers.append(number)
            
            
    return even_numbers
        
print(get_even([1,2,3,4,5,6,7,8,9,10])) """

def count_vowels(text):
    vowels = "aeiou"
    count = 0

    for char in text:
        if char in vowels:
            count +=1

    return count

print(count_vowels("Hello World"))