import lexico

def test(t):

    t1 = lexico.Lexico(t)
    t1.structure()
    t1.close()

if __name__ == '__main__':
    test("j.txt")
