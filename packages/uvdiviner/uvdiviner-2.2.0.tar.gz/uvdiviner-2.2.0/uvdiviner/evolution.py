try:
    from errors import TrigramValueError, TrigramsValueError, TrigramsTypeError
    from trigrams import data
except ImportError:
    from uvdiviner.errors import TrigramValueError, TrigramsValueError, TrigramsTypeError
    from uvdiviner.trigrams import data

class original:
    name = "无极"

class ultimate:
    name = "太极"

class diagram:
    def __init__(self, trigrams):
        if not isinstance(trigrams, list) and not isinstance(trigrams, tuple):
            raise TrigramsTypeError(type(trigrams))
        if len(trigrams) != 6:
            raise TrigramsValueError(len(trigrams))
        self.trigrams = trigrams
        self.status = "本卦"
        self.variated = 0
        self.data = None

        position = 0
        for trigram in trigrams:
            trigram.position = position
            position += 1

        self.update()

    def variate(self):
        if self.status == "变卦":
            raise NameError("当前已经是变卦, 不可以执行变卦指令.")

        for i in range(6):
            self.trigrams[i].variate()
            if self.trigrams[i].status == "变":
                self.variated += 1
        self.status = "变卦"
        
        self.update()
        return self
    
    def update(self):
        self.property = ""
        for trigram in self.trigrams:
            self.property += trigram.property
        
        self.name = [name for name in data.keys() if data[name]["属性"] == self.property]
        if len(self.name) == 0:
            print(Warning("Warning: 该卦尚未被录入."))
            self.name = "未知"
        else:
            self.name = self.name[0]
        
        number = ""
        for trigram in self.trigrams:
            number += str(trigram.number)
        self.number = int(number)

    def __int__(self):
        self.number

    def __repr__(self):
        return f"<diagram {self.number}>"

class trigram:
    def __init__(self, number):
        self.position = None
        if not number >= 6 or not number <= 9:
            raise TrigramValueError(number)

        if number == 6 or number == 8:
            self.property = "阴"
        else:
            self.property = "阳"

        if number == 6 or number == 9:
            self.status = "老"
        else:
            self.status = "少"

        self.number = number
        self.name = self.status + self.property

    def variate(self):
        if self.status == "老":
            self.status = "变"
            self.property = "阳" if self.property == "阴" else "阴"

    def __int__(self):
        return self.number
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<trigram {self.name}>"

evolutional_number = 55

if __name__ == "__main__":
    d = diagram(
        [trigram(9), trigram(9), trigram(9),
        trigram(9), trigram(9), trigram(9),]
        )
    print(d.status)
    print(d.name)
    print(d.property)
    print(d.number)
    d.variate()
    print(d.status)
    print(d.name)
    print(d.number)
    print(d.property)
