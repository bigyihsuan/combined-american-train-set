import re

TEMPLATE = re.compile(r"/^\/\/!SPRITES!\/\//")


def main():
    with open("cats-template.nml", "r") as templateFile, open("cats.nml", "w") as outputNML:
        templateNML = templateFile.read()
        [start, end] = TEMPLATE.split(templateNML)
        outputNML.write(start)
        # TODO: replace sprites
        outputNML.write(end)


if __name__ == "__main__":
    main()
