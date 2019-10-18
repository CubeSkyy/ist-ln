import sys

if len(sys.argv) != 3:
    raise ValueError("Usage: <Knowledge Base File> <Test File>")

inputName = sys.argv[1]
file = open(inputName, 'r')
file.close()
