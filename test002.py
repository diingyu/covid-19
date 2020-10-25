# print('hello world')

f=open('error.txt')
s=f.read()
print(s)
s=s.replace('\\\"','')
print(s)
