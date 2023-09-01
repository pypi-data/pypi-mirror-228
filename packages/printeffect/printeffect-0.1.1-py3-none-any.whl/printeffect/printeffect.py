import time, sys

NOREQ = False

def norequest():
    global NOREQ
    try:
        if NOREQ:
            NOREQ = False
        else:
            NOREQ = True
    except:
        NOREQ = False

def printeffect(testo, intervallo=None):
    global NOREQ
    try:
        NOREQ = NOREQ
    except:
        NOREQ = False
    if intervallo is None:
        if not NOREQ:
            print(f"Error: Missing argument")
            print("You must provide 2 arguments: printeffect(\"hello\", 0.07)")
            exit()
        else:
            intervallo = 0.07
            for carattere in testo:
                sys.stdout.write(carattere)
                sys.stdout.flush()
                time.sleep(intervallo)
            print()
    else:
        for carattere in testo:
            sys.stdout.write(carattere)
            sys.stdout.flush()
            time.sleep(intervallo)
        print()

def inputeffect(testo, intervallo):
    global NOREQ
    try:
        NOREQ = NOREQ
    except:
        NOREQ = False
    if intervallo is None:
        if not NOREQ:
            print(f"Error: Missing argument")
            print("You must provide 2 arguments: inputeffect(\"hello how are you? \", 0.07)")
        else:
            for carattere in testo:
                sys.stdout.write(carattere)
                sys.stdout.flush()
                time.sleep(intervallo)
            return input()
    else:
        for carattere in testo:
            sys.stdout.write(carattere)
            sys.stdout.flush()
            time.sleep(intervallo)
        return input()
