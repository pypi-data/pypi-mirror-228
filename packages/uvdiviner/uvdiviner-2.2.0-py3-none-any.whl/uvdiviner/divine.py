from typing import Dict
try:
    from uvdiviner.evolution import diagram, trigram, evolutional_number
    from uvdiviner.trigrams import data
    from uvdiviner.settings import DEBUG
except ImportError:
    from evolution import diagram, trigram, evolutional_number
    from trigrams import data
    from settings import DEBUG

import random

begin_number = evolutional_number - 6
explain = {
    0: "阳",
    1: "阴",
    2: "阳",
    3: "阴",
    4: "阳",
    5: "阴",
}

class Auspicious:
    def __init__(self, place, center, name: str="", variated_name: str=""):
        self.place = place
        self.center = center
        self.total = place + center
        self.name = f"{name}之{variated_name}"

    def __str__(self) -> str:
        if self.total >= 2:
            return "大吉"
        elif self.total == 1:
            return "小吉"
        elif self.total == 0:
            return "平"
        elif self.total == -1:
            return "小凶"
        elif self.total <= -2:
            return "大凶"

    def __bool__(self) -> bool:
        if self.total > 0:
            return True
        else:
            return False

def calculate(begin):
    sky = random.randint(1, begin)
    land = begin - sky - 1
    human = 1
    
    move_sky = sky % 4 if sky % 4 != 0 else 4
    move_land = land % 4 if land % 4 != 0 else 4
    
    sky = sky - move_sky
    land = land - move_land
    total = sky + land + human
    return (total, sky+land, sky, land, human)
    
def make_trigram():
    global begin_number
    first = calculate(begin_number)[0]
    second = calculate(first)[0]
    third = calculate(second)[1]
    trigram_number = int(third / 4)
    return trigram(trigram_number)

def divine():
    if not DEBUG:
        divined = diagram([make_trigram(), make_trigram(), make_trigram(), make_trigram(), make_trigram(), make_trigram()])
    else:
        divined = diagram([trigram(8), trigram(8), trigram(6), trigram(9), trigram(8), trigram(8)])

    return divined

def update_data(diagram):
    for d in data:
        if diagram.property == data[d]["属性"]:
            diagram.data = data[d]
    return diagram

def quick_check():
    place = 0
    center = 0
    diagram = update_data(divine())
    name = diagram.name
    novariate = diagram
    diagram.variate()
    variated_name = diagram.name

    changed = [trigram.position for trigram in diagram.trigrams if trigram.status == "变"]
    unchanged = [trigram.position for trigram in diagram.trigrams if trigram.status != "变"]
    trigrams: Dict[str, trigram] = {trigram.position: trigram for trigram in novariate.trigrams}

    num_changed = len(changed)
    if num_changed == 0:
        pass
    elif num_changed == 1:
        if explain[changed[0]] == trigrams[changed[0]].property:
            place += 1
        else:
            place -= 1
    elif num_changed == 2:
        if explain[changed[-1]] == trigrams[changed[-1]].property:
            place += 1
        else:
            place -= 1
    elif num_changed == 3:
        pass
    elif num_changed == 4:
        if explain[changed[0]] == trigrams[unchanged[0]].property:
            place += 1
        else:
            place -= 1
    elif num_changed == 5:
        if explain[changed[-1]] == trigrams[unchanged[0]].property:
            place += 1
        else:
            place -= 1
    else:
        pass

    if 1 in changed:
        center += 1

    if 4 in changed:
        center += 1

    if 4 not in changed and 1 not in changed:
        center -= 1

    return Auspicious(place, center, name=name, variated_name=variated_name)

if __name__ == "__main__":
    qc = quick_check()
    if qc:
        print("通过.")
    print(qc)
    print(qc.name)