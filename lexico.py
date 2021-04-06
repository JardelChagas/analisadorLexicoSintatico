import pandas as pd

class Lexico:
    def __init__(self, file):
        self.file = open(file)
        self.dir = file
        self.out = pd.DataFrame(columns=["Lexema", "Padrão", "Token", "Linha"])
        self.symbolTable = pd.DataFrame(columns=["value", "number" ])
        self.lexemasReserveString = [
            "class",
            "public",
            "static",
            "void",
            "main",
            "String",
            "extends",
            "return",
            "int",
            "boolean",
            "if",
            "while",
            "System.out.println",
            "length",
            "true",
            "false",
            "new"
        ]
        self.symbols = [
            "(", ")",
            "[", "]",
            "{", "}",
            "<", "+", "-", "*", ".", "!", ";"
        ]
        self.stackK = [] #pilha de chaves
        self.stackP = [] #pilha de parenteses
        self.stackC = [] #pilha de cochetes
        self.stack  = []
        self.countIdentifier = 0

    def structure(self):
        list = self.mainClass()
        if list != "":
            self.classDeclaration(list[0], list[1])
        print(self.out)
        print(self.symbolTable)
        '''if 'Test' == self.symbolTable.iloc[0]['value']:
            for st in self.symbolTable['value']:
                print(end="")'''

    def mainClass(self):
        mc = ["class", "Identifier", "{", "public", "static", "void", "main", "(", "String", "[", "]", "Identifier", ")",
              "{", "Statement", "}", "}"]
        token = ""

        countLine = 0
        est = 0
        for line in self.file:
            countLine += 1
            i = 0
            if est < len(mc):
                while i < len(line):
                    if line[i] != " " and line[i] != "" and line[i] != "\n":
                        token += line[i]
                        #print(token)
                        if token == mc[est] or mc[est] == "Identifier" or mc[est] == "Statement":
                            if mc[est] == "Identifier":
                                l = self.identifier(line, i)
                                if l == "":
                                    print("erro line ", countLine)
                                    return ""
                                else:
                                    self.countIdentifier += 1
                                    self.createRow(l[0], countLine)
                                    self.symbolTable = self.symbolTable.append(
                                        {"value": l[0], "number": self.countIdentifier}, ignore_index=True)

                                    i = l[2] - 1
                                    token = ""
                                est += 1
                            elif mc[est] == "Statement":
                                self.statement(0, countLine)
                                est += 1
                                i = len(line)
                                token = ""
                            elif mc[est] in self.symbols:
                                for j in range(len(self.symbols)):
                                    if mc[est] == self.symbols[j]:
                                        if j % 2 == 0:
                                            self.createRow(token, countLine)
                                            self.stack.append("#")
                                            break
                                        else:
                                            self.createRow(token, countLine)
                                            self.stack.pop()
                                            break
                                est += 1
                                token = ""
                            else:
                                self.createRow(token, countLine)
                                token = ""
                                est += 1

                        else:
                            if self.isErr(token, mc, countLine) and self.isErr(token, self.symbols, countLine):
                                print("erro! Simbolo invalido na linha ", token, countLine)
                                return ''
                    i += 1
        return [line, i]

    def classDeclaration(self, r, countLine):
        cd  = ["class", "Identifier", "extends", "Identifier", "{", "VarDeclaration", "MethodDeclaration", "}"]
        tk  = ''
        est = 0
        for line in self.file:
            for e in line:
                if e != " " and e != "" and e != "\n":
                    tk += e
                    if tk == cd[est]:
                        self.createRow(token, countLine)
                        token = ''
                        est += 1
                    elif cd[est] == "Identifier":
                        l = self.identifier(line, i)
                        if l == '':
                            print("erro line ", countLine)
                            return ''
                        else:
                            self.countIdentifier += 1
                            self.createRow(l[0], countLine)
                            self.symbolTable = self.symbolTable.append(
                                {"value": l[0], "number": self.countIdentifier}, ignore_index=True)
                            i = l[2] - 1
                            token = ''
                            est += 1
                    elif (est == 2 or est == 4) and tk == "{":
                        self.createRow('{', countLine)
                        est = 5
                        tk = ''

    def methodDeclaration(self):
        print(end='')

    def statement(self, i, countLine):
        file = open(self.dir)
        cont = 0
        tk = ""
        for line in file:
            cont += 1
            if cont >= countLine:
                if not "=" in line:
                    while i < len(line):
                        if line[i] != " " and line[i] != "" and line[i] != "\n":
                            tk += line[i]
                            if tk == "System.out.println":
                                self.createRow(tk, cont)
                                i += 1
                                if line[i] != " " and line[i] != "" and line[i] != "\n":
                                    if line[i] == "(":
                                        self.createRow(line[i], cont)
                                        li = self.expression(i+1, countLine)
                                        i = li[0]
                                        if not (line[i] in self.symbols):
                                            print("erro in line ", countLine)
                                            print(line[i], end="")
                                            return ""
                                    #if l[i] == ")":
                                    #    self.createRow(l[i], cont)
                                    #    i += 1
                                    if line[i] == ";":
                                        self.createRow(line[i], cont)

                                        return [i, cont]
                            elif tk == "{":
                                self.createRow(tk, countLine)
                                tk = ''
                                aux = self.statement(i+1, countLine)
                                i = aux[0]
                                while i < len(line):
                                    if line[i] != " " and line[i] != "" and line[i] != "\n":
                                        if line[i] == "}":
                                            self.createRow(line[i], countLine)

                                    i += 1
                            elif tk == "if(":
                                self.createRow("if", countLine)
                                self.createRow("(", countLine)
                                li = self.expression(i+1, countLine)

                                i = li[0]
                                if line[i] == "{":
                                    self.createRow("{", countLine)
                                    self.statement(0, countLine+1)
                                    countLine += 1
                                tk = ''
                            elif tk == "else{":
                                self.createRow("else", countLine)
                                self.createRow("{", countLine)
                                self.statement(i+1, countLine)
                                countLine += 1

                                tk = ''
                            elif tk == 'while(':
                                self.createRow("while", countLine)
                                self.createRow("(", countLine)
                                li = self.expression(i+1, countLine)
                                i = li[0]
                                if line[i] == "{":
                                    self.createRow("{", countLine)
                                    self.statement(0, countLine + 1)
                                    countLine += 1
                                tk = ''
                            elif tk == "}":
                                self.createRow("}", countLine)
                                tk = ''

                        i += 1
                    i = 0
                    countLine += 1
                else:
                    if "[" in line and "]" in line and "=" in line:
                        l = line.split("[")
                        for r in l[0]:
                            if r != " " and r != "" and r != "\n":
                                aux += r
                        self.createRow(aux, countLine)
                        self.createRow("[", countLine)
                        self.expression(len(l[0] + 1), countLine)
                    else:
                        l = line.split("=")
                        self.countIdentifier += 1
                        aux = ""
                        for r in l[0]:
                            if r != " " and r != "" and r != "\n":
                                aux += r
                        self.createRow(aux, countLine)
                        self.createRow("=", countLine)
                        self.expression(len(l[0]+1), countLine)


        return [i, cont]

    def expression(self, r, countLine):
        file = open(self.dir)
        cl = 0
        symbols = [".", "(", ")", "[", "]", "!", "&", "&&" "<", "+", "-", "*"]
        strings = ["true", "false", "this", "new", "int", "length"]
        tk = ''
        for line in file:
            cl += 1
            if cl == countLine:

                while r < len(line):
                    if (line[r] >= 'a' and line[r] <= 'z') or (line[r] >= 'A' and line[r] <= 'Z') or(line[r] >= '0' and line[r] <= '9') or (line[r] == "_"):
                        tk += line[r]
                    elif line[r] != " " and line[r] != "" and line[r] != "\n":
                        #para entrar aki tem que ser diferente de letras e numeros e espaço vazio
                        if tk != '':
                            if line[r] in symbols:
                                if tk in strings:
                                    self.createRow(tk, countLine)
                                    tk = ''
                                    self.createRow(line[r], countLine)
                                else:
                                    #saber se é um indetifile
                                    for st in self.symbolTable['value']:
                                        if tk == st:
                                            self.createRow(tk, countLine)
                                            tk = ''
                                            if line[r] in symbols:
                                                self.createRow(line[r], countLine)
                                            else:
                                                return [r, tk]

                                    self.createRow(tk, countLine)
                                    tk = ''
                                    if line[r] in symbols:
                                        self.createRow(line[r], countLine)

                            else:
                                self.createRow(tk, countLine)#

                                return [r, tk]
                        else:
                            if line[r] in symbols:
                                self.createRow(line[r], countLine)
                            else:
                                return [r, tk]
                    else:
                        if tk != '':
                            self.createRow(tk, countLine)
                            tk = ''
                    r += 1

                return [r, tk]

    def varDeclaration(self, line, i, countLine):
        l = self.type(line, i, countLine)
        if l != '':
            self.identifier(l[0], l[1])
        if ";" in line:
            self.createRow(";", countLine)
    '''-ok-'''
    def type(self, line, i, countLine):
        l = line[i:].split(" ")
        list = ["int", "boolean", "int[]", "int["]
        if l[0] in list:
           if (l[0] == "int" and l[1] == "[" and l[2] == "]") or (l[0] == "int[" and l[1] == "]") or (l[0] == "int" and l[1] == "[]") or l[0] == "int[]":
               self.createRow("int", countLine)
               self.createRow("[", countLine)
               self.createRow("]", countLine)
           else:
               self.createRow(l[0], countLine)
        else:
            l = self.identifier(line, i)
            if l == "":
                print("erro line ", countLine)
                return ""
            else:
                self.countIdentifier += 1
                self.createRow(l[0], countLine)
                self.symbolTable = self.symbolTable.append(
                    {"value": l[0], "number": self.countIdentifier}, ignore_index=True)

        '''
        for r in line:
            if r != " " and r != "" and r != "\n":
                token += + r
            elif token != "":
                if token in list:
                    print(end="")
        '''
    '''-ok-'''
    def identifier(self, line, i):
        stt = 1
        txt = ""
        for b in range(len(line)):
            b = i
            if txt == "":
                if line[b] >= "a" and line[b] <= "z":
                    txt += line[b]
                elif line[b] >= "A" and line[b] <= "Z":
                    txt += line[b]
                elif line[b] == "_":
                    txt += line[b]
                elif line[b] != " " and line[b] != "" and line[b] != "\n":
                    return ""
            else:
                if line[b] >= "a" and line[b] <= "z":
                    txt += line[b]
                elif line[b] >= "A" and line[b] <= "Z":
                    txt +=line[b]
                elif line[b] >= "0" and line[b] <= "9":
                    txt +=line[b]
                elif line[b] == "_":
                    txt +=line[b]
                else:
                    if txt in self.lexemasReserveString:
                        print("palavra reservada")
                        return ""
                    else:
                        return [txt, line, b]
            i += 1
    '''---------------------------------'''
    def createRow(self, aux, cont):
        tk = self.createToken(aux, cont)
        stdd = self.pattern(aux)
        self.out = self.out.append(
            {"Lexema": aux, "Padrão": stdd, "Token": tk, "Linha": cont},
            ignore_index=True)

    def createToken(self, text, cont):
        if text not in self.lexemasReserveString and text not in self.symbols:
            if text[0] >= "0" and text[0] <= "9":
                return "<Number, >"
            #for st in self.symbolTable['value']:
             #   if st == text:

            return "<Identifier, " + str(cont) + ">"
        return "<" + text + ",>"

    def pattern(self, text):
        for r in self.lexemasReserveString:
            if (r == text):
                return "ReserveString"
        for r in self.symbols:
            if r == text:
                return r
        for r in text:
            if r >= "0" and r <= "9":
                return "Number"
        return "Identifier"

    def isErr(self, token, mc, countLine):
        err = False
        for r in token:
            for palavra in mc:
                for letra in palavra:
                    if r == letra:
                        err = False
                        break
                    else:
                        err = True
                if not err:
                    break
            if err:
                return err
        return err
    def number(self, n, l):#"ac323"
        number = ""
        for i in len(l):
            if i >= n:
                if l[i] >= "0" and l[i] <= "9":
                    number += l[i]
                elif number != "":
                    return [number, i]

    def close(self):
        self.file.close()