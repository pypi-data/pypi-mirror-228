class TrigramValueError(ValueError):
    def __init__(self, message):
        super().__init__(self)
        self.message = "警告: 卜筮中所得到的爻数必须是 6 到 9 之间的正整数, 而传入的爻数为 %d, 这可能是算法错误或上层叙事者的一次叙事. 请优先检验算法问题." % message
    
    def __str__(self):
        return self.message
 
class TrigramsValueError(ValueError):
    def __init__(self, message):
        super().__init__(self)
        self.message = "卦爻数必须是 6 个, 但你传入了 %d 个数据." % message

    def __str__(self):
        return self.message

class TrigramsTypeError(TypeError):
    def __init__(self, message):
        super().__init__(self)
        self.message = "卦爻必须是 List 或者 Tuple 数据, 但你传入的是 %s." % message

    def __str__(self):
        return self.message
