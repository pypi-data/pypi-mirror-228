import time, sys
def inputeffect(testo, intervallo):
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(intervallo)
    return input()