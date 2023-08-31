import time, sys
def printeffect(testo, intervallo):
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(intervallo)
    print()
def inputeffect(testo, intervallo):
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(intervallo)
    return input()