from termcolor import colored
import quartz

def printTxt(txt, clr):
    print(colored(txt, clr))

printTxt("Quartz - Alpha v1.0.2", "green")

while True:
    text = input("\n> ");
    if not text:
        continue
    result, error = quartz.run("<console>", text)

    if error:
        printTxt(error.as_string(), "red")
    else:
        print("  " + str(result))






