import lexico

def test(t):
    t1 = lexico.Lexico(t)
    t1.structure()
    t1.close()
def aki():
    l = "jardel torres"
    c = " t"
    if c in l:
        print("c")
    else:
        print("aushuashauha")

if __name__ == '__main__':
    test("j.txt")
