try:
    from uvdiviner.evolution import diagram, trigram
    from uvdiviner.trigrams import data
    from uvdiviner.progressbar import ProgressBar
    from uvdiviner.divine import make_trigram, update_data
    from uvdiviner.colorize import bright, light_white, cyan, light_green, light_red, light_magenta, light_yellow
    from uvdiviner.settings import DEBUG
except ImportError:
    from evolution import diagram, trigram
    from trigrams import data
    from progressbar import ProgressBar
    from divine import make_trigram, update_data
    from colorize import bright, light_white, cyan, light_green, light_red, light_magenta, light_yellow
    from settings import DEBUG

import time
import sys

def clear_output():
    sys.stdout.write('\033[1J')
    sys.stdout.write('\033[H')
    sys.stdout.flush()

def get_useful_data(diagram):
    result = ""

    update_data(diagram)
    static = diagram.data
    static["卦名"] = diagram.name + "卦"
    diagram.variate()
    update_data(diagram)
    variable = diagram.data
    variable["卦名"] = diagram.name + "卦"

    if diagram.variated == 0:
        result += "    象: " + static["象"] + "\n"
        result += "    彖: " + static["彖"] + "\n\n"
        result += cyan("该卦为静卦, 不存在动爻, 请从本卦卦辞、象和彖中获得有效卜筮结果.")
    elif diagram.variated == 1:
        for trigram in diagram.trigrams:
            if trigram.status == "变":
                result += light_yellow(static["卦名"]) + " 变爻爻辞: \n"
                result += "    " + light_green(static["爻辞"][trigram.position])
                result += "\n\n"
        result += cyan("此卦共 1 爻动, 请以本卦变爻爻辞为核心断解此次卜筮结果.")
    elif diagram.variated == 2:
        result += light_yellow(static["卦名"]) + " 变爻爻辞: \n"
        for trigram in diagram.trigrams:
            if trigram.status == "变":
                result += "    " + light_green(static["爻辞"][trigram.position]) + "\n"
        result += "\n"
        result += cyan("此卦共 2 爻动, 请以本卦变爻爻辞为核心断解此次卜筮结果, 其中上变爻权重大于下变爻.")
    elif diagram.variated == 3:
        result = cyan("此卦共 3 爻动, 请结合本卦卦辞和变卦卦辞, 两两结合, 断解此次卜筮结果.")
        static["卦辞"] = light_green(static["卦辞"])
        variable["卦辞"] = light_green(variable["卦辞"])
    elif diagram.variated == 4:
        result += light_yellow(variable["卦名"]) + " 变爻爻辞: \n"
        for trigram in diagram.trigrams:
            if trigram.status != "变":
                result += "    " + light_green(variable["爻辞"][trigram.position]) + "\n"
        result += "\n"
        result += cyan("此卦共 4 爻动, 请以变卦不变爻爻辞为核心断解此次卜筮结果, 其中下爻权重大于上爻.")
    elif diagram.variated == 5:
        result += light_yellow(variable["卦名"]) + " 不变爻爻辞: \n"
        for trigram in diagram.trigrams:
            if trigram.status != "变":
                result += "    " + light_green(static["爻辞"][trigram.position]) + "\n"
        result += "\n"
        result += cyan("此卦共 5 爻动, 请以变卦不变爻爻辞为核心断解此次卜筮结果.")
    elif diagram.variated == 6:
        if not static["卦名"][:-1] in ["乾", "坤"]:
            result += "原爻爻辞: \n"
            for trigram in diagram.trigrams:
                if trigram.status != "变":
                    result += "    " + static["爻辞"][trigram.position] + "\n"
            result += "\n"
            result += cyan("此卦六爻全动, 请以变卦卦辞为核心断解此次卜筮结果.")
        else:
            result += light_magenta("本卦断解: \n    ")
            result += light_green(static["爻辞"][6])
            result += "\n\n"
            name = "用九" if static["卦名"][:-1] == "乾" else "用六"
            result += cyan("此卦为 " + static["卦名"][:-1] + "之" + variable["卦名"][:-1] + f", 六爻全动, 请以 {name} 的爻辞为核心断解此次卜筮结果.")

    return static, variable, result

def main():
    global DEBUG

    if not DEBUG:
        y = True if input(
            bright(light_white("警告: 不建议在短时间内执行大量卜筮行为, 这可能会导致气运大幅下降. (已知悉? y/n) "))
            ) in ["y", "yes", "Y", "YES"] else False
        if not y:
            print("占卜者未确认, 已终止.")
            return
    clear_output()
    
    print(
        "\r" + light_red(
        "天何言哉，叩之即应；神之灵矣，感而遂通。\n"
        "今有某人，有事关心，罔知休咎，罔释厥疑，\n"
        "惟神惟灵，望垂昭报，若可若否，尚明告之。\n"
        ),
        flush = True,
        )

    trigrams = [make_trigram(), make_trigram(), make_trigram(),] if not DEBUG else [trigram(8), trigram(8), trigram(6),]

    for i in range(1, 28):
        ProgressBar(i/55, name="内卦")
        if not DEBUG:
            time.sleep(1)

    print(light_red("\n\n" "某宫三象，吉凶未判，再求外象三爻，以成一卦，以决忧疑。" "\n"))

    for i in range(28, 56):
        ProgressBar(i/55, name="外卦")
        if not DEBUG:
            time.sleep(1)

    trigrams += [make_trigram(), make_trigram(), make_trigram()] if not DEBUG else [trigram(9), trigram(8), trigram(8)]
    print("\n")

    if not DEBUG: time.sleep(1)

    dia = diagram(trigrams)

    static, variable, result = get_useful_data(dia)

    if not static["卦名"] == variable["卦名"]:
        print(
            light_magenta("占卜结果:"),
            light_yellow(static["卦名"][:-1] + "之" + variable["卦名"][:-1]),
            "\n"
            )
    else:
        print("占卜结果:", static["卦名"], "\n")
    
    if not DEBUG: time.sleep(1)

    print("本卦:", light_yellow(static["卦名"]))
    print("   ", "卦辞:", light_green(static["卦辞"]), "\n")

    if not DEBUG: time.sleep(1)

    if dia.variated != 0:
        print("变卦:", light_yellow(variable["卦名"]))
        print("   ", "卦辞:", light_green(variable["卦辞"]), "\n")
        print("变爻数:", dia.variated, "\n")
    
    if not DEBUG: time.sleep(2)

    print(result)

if __name__ == "__main__":
    main()