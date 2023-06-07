class Test:
    number = 10
    color = 'red'
    def soft():
        print(Test.number, Test.color)#calling variables from class with class mention
Test.soft()#calling function directly. There is no arguments

class Test:
    number = 10
    color = 'red'
    def dark(self):
        print('dark is worked')
    def light(self):
        print('light is worked')
    def soft(self):
        print('soft is worked')
func = Test()# if we will call copy of class we would get an error, because there is one argument in copy - link to the class
func.soft()# thats why we must put an argument in class function as "self"
func.dark()
func.light()
Test.soft(func)# now we cant call class with no arguments, cuz we put "self" in class function. Then we put copy as argument