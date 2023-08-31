import time, sys
def printe(testo, intervallo):
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(intervallo)
    print()
def inpute(testo, intervallo):
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(intervallo)
    return input()