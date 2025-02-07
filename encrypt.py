from functions import *
import json
import sys


NUM_ROUNDS = 16
DEFAULT_M = 0x0123456789ABCDEF
DEFAULT_K = 0x0123456789ABCDEF


if __name__ == "__main__":

    M = DEFAULT_M
    if (len(sys.argv) >= 2):
        try: M = int(sys.argv[1]) & 0xFFFFFFFFFFFFFFFF
        except ValueError: pass
    
    K = DEFAULT_K
    if (len(sys.argv) >= 3):
        try: M = int(sys.argv[2]) & 0xFFFFFFFFFFFFFFFF
        except ValueError: pass

    with open('tables.json', 'r') as file:
        tables = json.load(file)

    pM = permute(M, tables["IP"], 64)
    L,R = split(pM, 64)
    pK = permute(K, tables["PC1"], 64)
    C,D = split(pK, 56)

    print()
    print(f"           Plaintext                                       Key")
    print(f"       {fHex(M,64)}                           {fHex(K,64)}")
    print(f"    ┏━━━━━━━━━━┷━━━━━━━━━━┓                       ┏━━━━━━━━━┷━━━━━━━━━┓")
    print(f"    ┃ Initial Permutation ┃                       ┃ Permuted Choice 1 ┃")
    print(f"    ┗━━━━━━━━━━┯━━━━━━━━━━┛                       ┗━━━━━━━━━┯━━━━━━━━━┛")
    print(f"       {fHex(pM,64)}                            {fHex(pK,56)}")
    print(f"     ┌─────────┴─────────┐                        ┌─────────┴─────────┐")
    for i in range(NUM_ROUNDS):
        numR = tables["R"][i]

        print(f"     L{fDec(i)}                 R{fDec(i)}                      C{fDec(i)}                 D{fDec(i)}")
        print(f" {fHex(L,32)}          {fHex(R,32)}               {fHex(C,28)}           {fHex(D,28)}")
        print(f"     │  ┌────────────────┤                        │                   │")
        print(f"     │  │          ┏━━━━━┷━━━━━┓          ┏━━━━━━━┷━━━━━━━━┓  ┏━━━━━━━┷━━━━━━━━┓")
        print(f"     │  │          ┃ Expansion ┃          ┃ Left Shift ({numR}) ┃  ┃ Left Shift ({numR}) ┃")

        ER = permute(R, tables["E"], 32)
        C, D = rotate(C,28,numR), rotate(D,28,numR)
        Ki = permute(combine(C,D,56), tables["PC2"], 56)
        A = ER ^ Ki
        S = [(A>>(6*(7-i)))&63 for i in range(8)]


        print(f"     │  │          ┗━━━━━┯━━━━━┛          ┗━━━━━━━┯━━━━━━━━┛  ┗━━━━━━━┯━━━━━━━━┛")
        print(f"     │  │                │                  ┌─────┴─────┐       ┌─────┴─────┐")
        print(f"     │  │              E[R{(str(i)+']').ljust(3)}               │     ┏━━━━━┷━━━━━━━┷━━━━━┓     │")
        print(f"     │  │          {fHex(ER,48)}           │     ┃ Permuted Choice 2 ┃     │")
        print(f"     │  │                │                  │     ┗━━━━━━━━━┯━━━━━━━━━┛     │")
        print(f"     │  │              ┏━┷━┓                │       K{fDec(i+1)}     │               │")
        print(f"     │  │              ┃XOR┠────────────────┼─{fHex(Ki,48)}┘               │")
        print(f"     │  │              ┗━┯━┛                │                               │")
        print(f"     │  │  ┌───┬───{fHex(A,48)}──┬───┐    │                               │")
        print(f"     │  │ {fHex(S[0],8)} │  {fHex(S[2],8)} │  {fHex(S[4],8)} │  {fHex(S[6],8)} │    │                               │")
        print(f"     │  │  │ {fHex(S[1],8)}  │ {fHex(S[3],8)}  │ {fHex(S[5],8)}  │ {fHex(S[7],8)}   │                               │")
        print(f"     │  │  │   │   │   │   │   │   │   │    │                               │")

        S = [sBox(S[i], tables['S'][i]) for i in range(8)]
        B = sum(S[i]<<((7-i)*4) for i in range(8))
        PB = permute(B, tables['P'], 32)

        print(f"     │  │ {fHex(S[0],4)}  │  {fHex(S[2],4)}  │  {fHex(S[4],4)}  │  {fHex(S[6],4)}  │    │                               │")
        print(f"     │  │  │  {fHex(S[1],4)}  │  {fHex(S[3],4)}  │  {fHex(S[5],4)}  │  {fHex(S[7],4)}   │                               │")
        print(f"     │  │  └───┴───┴─{fHex(B,32)}┴───┴───┘    │                               │")
        print(f"     │  │         ┏━━━━━━┷━━━━━━┓           │                               │")
        print(f"     │  │         ┃ Permutation ┃           │                               │")
        print(f"     │  │         ┗━━━━━━┯━━━━━━┛           └─────┐                   ┌─────┘")
        print(f"     │  │            {fHex(PB,32)}                   │                   │")
        print(f"     │  │              ┏━┷━┓                      │                   │")
        print(f"     └──┼──────────────┨XOR┃                      │                   │")
        print(f"     ┌──┘              ┗━┯━┛                      │                   │")

        L, R = R, PB ^ L

    C = combine(R, L, 64)

    print(f"     L{fDec(i+1)}                 R{fDec(i+1)}                      X                   X")
    print(f" {fHex(L,32)}          {fHex(R,32)}")
    print(f"     └───────┐       ┌───┘")
    print(f"        {fHex(C,64)}")
    print(f"  ┏━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┓")
    print(f"  ┃ Inverse Initial Permutation ┃")
    print(f"  ┗━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┛")
    print(f"                 │")

    C = permute(C, tables["IP1"], 64)

    print(f"            Ciphertext")
    print(f"        {fHex(C,64)}")
    print()
