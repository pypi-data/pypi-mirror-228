import time, sys, inspect

_NOREQ = False

def norequest():
    if _NOREQ:
        _NOREQ = False
    else:
        _NOREQ = True
def printeffect(testo, intervallo):
    try:
        for carattere in testo:
            sys.stdout.write(carattere)
            sys.stdout.flush()
            time.sleep(intervallo)
        print()
    except TypeError as e:
        if _NOREQ == False:
            if "required positional argument" in str(e):
                params = inspect.signature(printeffect).parameters
                missing_args = [param for param in params if params[param].default == inspect.Parameter.empty]
                print(f"Errore: Mancano gli argomenti {', '.join(missing_args)}")
                print("You must provide 2 arguments: printeffect(\"hello\", 0.07)")
            else:
                print("Errore: Si è verificato un errore sconosciuto.")
        else:
            for carattere in testo:
                sys.stdout.write(carattere)
                sys.stdout.flush()
                time.sleep(0.07)
            print()
def inputeffect(testo, intervallo):
    try:
        for carattere in testo:
            sys.stdout.write(carattere)
            sys.stdout.flush()
            time.sleep(intervallo)
        return input()
    except TypeError as e:
        if _NOREQ == False:
            if "required positional argument" in str(e):
                params = inspect.signature(printeffect).parameters
                missing_args = [param for param in params if params[param].default == inspect.Parameter.empty]
                print(f"Errore: Mancano gli argomenti {', '.join(missing_args)}")
                print("You must provide 2 arguments: printeffect(\"hello\", 0.07)")
            else:
                print("Errore: Si è verificato un errore sconosciuto.")
        else:
            for carattere in testo:
                sys.stdout.write(carattere)
                sys.stdout.flush()
                time.sleep(0.07)
            return input()