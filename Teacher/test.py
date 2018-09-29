
def sums(list,target,partial=[]):
    s = sum(partial)
    if s == target:
        print("s=",s,"parital=",partial)
        return partial

    for i in range(len(list)):
        n = list[i]

        remaining = list[i+1:]
        sums(remaining,target,partial+[n])

#partial = sums([1,2,3,4,5,6],6)

def sum1(list,target, partial = []):
    s = sum(partial)

    if s == target:
        print("parital = ",partial)
        return partial

    for i in range(len(list)):
        n = list[i]
        remaining = list[i+1:]
        sum1(remaining,target,partial+[n])

#sum1([1,2,3,4,5,6,7],6)



def sum2(list,target, partial = []):
    s = sum(partial)

    if s == target:
        print(partial)
        return partial

    for i in range(len(list)):
        n = list[i]
        remaining = list[i+1:]
        sum2(remaining,target,partial+[n])

#sum2([6,5,4,3,2,1,1],6)


var = "I am a string"
print(var.split(' '))

class Employee:
    secretCount = 0
    __secretCount1 =0

    def __init__(self):
        self.secretCount += 1
        self.__secretCount1 +=1

e = Employee()
print(e.secretCount)













