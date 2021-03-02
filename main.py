from termcolor import colored
import quartz

def printTxt(txt, clr):
    print(colored(txt, clr))

printTxt("Quartz - Alpha v1.0.1", "cyan")

while True:
    text = input("\n> ");
    result, error = quartz.run("<stdin>", text)

    if error:
        printTxt(error.as_string(), "red")
    else:
        print("  " + str(result))






