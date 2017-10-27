first = 'Sueaaaaa'
last = 'Wong'
name = first + ' ' + last

su=first
su

x=3
y=5
print('The sum of', x, 'plus', y, 'is', x+y)



sillyTest = '''Say,
"I'm in!"
This is line 3'''
print(sillyTest)

print('Hello world')

person = input('Enter your name: ')
greeting = 'Hello {}!'.format(person)
print(greeting)


applicant = input("Enter the applicant's name: ")
interviewer = input("Enter the interviewer's name: ")
time = input("Enter the appointment time: ")
print(interviewer + ' will interview ' + applicant + ' at ' + time +'.')
print(interviewer, ' will interview ', applicant, ' at ', time, '.', sep='')
print('{} will interview {} at {}.'.format(interviewer, applicant, time))


x = 20
y = 30
formatStr = '{0} + {1} = {2}; {0} * {1} = {3}.'
equations = formatStr.format(x, y, x+y, x*y)
print(equations)


def sumProblem(x, y):
    sum = x + y
    print('The sum of '+x+ ' and '+y+' is '+sum+'.', sep="x")
def main():
    sumProblem(2, 3)
    sumProblem(1234567890123, 535790269358)
    a = int(input("Enter an integer: "))
    b = int(input("Enter another integer: "))
    sumProblem(a, bdev
main()

t = (23, 'abc', 4.56, (2,3), 'def')

d = {'user':'bozo', 'pswd':1234}
f = json.dumps(d, sort_keys=True, indent=2)
filename="1.json"

json_data = f.json_format_dict(d, True)
cache = open(filename, 'w')
cache.write(json_data)
cache.close()
