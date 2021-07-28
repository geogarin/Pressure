def a():
    print('aaa')

def b():
    print('bbb')


if __name__=='__main__':
    c=[]
    c.append(a)
    c.append(b)

    c[1]()
    c[0]()

