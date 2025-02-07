# DES Simulator

This script simulates DES step by step, showing the results along the way. This started as a simple script to help me with my cryptography homework, but then I thought it would be cool to build out.

## Usage:

```bash
python encrypt.py [message] [key]
```

## Example:

Here is an example using 2 rounds of encryption instead of the standard 16:

```
           Plaintext                                       Key
       0x0123456789ABCDEF                           0x0123456789ABCDEF
    ┏━━━━━━━━━━┷━━━━━━━━━━┓                       ┏━━━━━━━━━┷━━━━━━━━━┓
    ┃ Initial Permutation ┃                       ┃ Permuted Choice 1 ┃
    ┗━━━━━━━━━━┯━━━━━━━━━━┛                       ┗━━━━━━━━━┯━━━━━━━━━┛
       0xCC00CCFFF0AAF0AA                            0xF0CCAA0AACCF00
     ┌─────────┴─────────┐                        ┌─────────┴─────────┐
     L0                  R0                       C0                  D0
 0xCC00CCFF          0xF0AAF0AA               0xF0CCAA0           0xAACCF00
     │  ┌────────────────┤                        │                   │
     │  │          ┏━━━━━┷━━━━━┓          ┏━━━━━━━┷━━━━━━━━┓  ┏━━━━━━━┷━━━━━━━━┓
     │  │          ┃ Expansion ┃          ┃ Left Shift (1) ┃  ┃ Left Shift (1) ┃
     │  │          ┗━━━━━┯━━━━━┛          ┗━━━━━━━┯━━━━━━━━┛  ┗━━━━━━━┯━━━━━━━━┛
     │  │                │                  ┌─────┴─────┐       ┌─────┴─────┐
     │  │              E[R0]                │     ┏━━━━━┷━━━━━━━┷━━━━━┓     │
     │  │          0x7A15557A1555           │     ┃ Permuted Choice 2 ┃     │
     │  │                │                  │     ┗━━━━━━━━━┯━━━━━━━━━┛     │
     │  │              ┏━┷━┓                │       K1      │               │
     │  │              ┃XOR┠────────────────┼─0x0B02679B49A5┘               │
     │  │              ┗━┯━┛                │                               │
     │  │  ┌───┬───0x711732E15CF0──┬───┐    │                               │
     │  │ 0x1C │  0x1C │  0x38 │  0x33 │    │                               │
     │  │  │ 0x11  │ 0x32  │ 0x15  │ 0x30   │                               │
     │  │  │   │   │   │   │   │   │   │    │                               │
     │  │ 0x0  │  0x2  │  0x6  │  0x5  │    │                               │
     │  │  │  0xC  │  0x1  │  0xD  │  0x0   │                               │
     │  │  └───┴───┴─0x0C216D50┴───┴───┘    │                               │
     │  │         ┏━━━━━━┷━━━━━━┓           │                               │
     │  │         ┃ Permutation ┃           │                               │
     │  │         ┗━━━━━━┯━━━━━━┛           └─────┐                   ┌─────┘
     │  │            0x921C209C                   │                   │
     │  │              ┏━┷━┓                      │                   │
     └──┼──────────────┨XOR┃                      │                   │
     ┌──┘              ┗━┯━┛                      │                   │
     L1                  R1                       C1                  D1
 0xF0AAF0AA          0x5E1CEC63               0xE199541           0x5599E01
     │  ┌────────────────┤                        │                   │
     │  │          ┏━━━━━┷━━━━━┓          ┏━━━━━━━┷━━━━━━━━┓  ┏━━━━━━━┷━━━━━━━━┓
     │  │          ┃ Expansion ┃          ┃ Left Shift (1) ┃  ┃ Left Shift (1) ┃
     │  │          ┗━━━━━┯━━━━━┛          ┗━━━━━━━┯━━━━━━━━┛  ┗━━━━━━━┯━━━━━━━━┛
     │  │                │                  ┌─────┴─────┐       ┌─────┴─────┐
     │  │              E[R1]                │     ┏━━━━━┷━━━━━━━┷━━━━━┓     │
     │  │          0xAFC0F9758306           │     ┃ Permuted Choice 2 ┃     │
     │  │                │                  │     ┗━━━━━━━━━┯━━━━━━━━━┛     │
     │  │              ┏━┷━┓                │       K2      │               │
     │  │              ┃XOR┠────────────────┼─0x69A659256A26┘               │
     │  │              ┗━┯━┛                │                               │
     │  │  ┌───┬───0xC666A050E920──┬───┐    │                               │
     │  │ 0x31 │  0x1A │  0x14 │  0x24 │    │                               │
     │  │  │ 0x26  │ 0x20  │ 0x0E  │ 0x20   │                               │
     │  │  │   │   │   │   │   │   │   │    │                               │
     │  │ 0x5  │  0x4  │  0x3  │  0xB  │    │                               │
     │  │  │  0xB  │  0xA  │  0x8  │  0x7   │                               │
     │  │  └───┴───┴─0x5B4A38B7┴───┴───┘    │                               │
     │  │         ┏━━━━━━┷━━━━━━┓           │                               │
     │  │         ┃ Permutation ┃           │                               │
     │  │         ┗━━━━━━┯━━━━━━┛           └─────┐                   ┌─────┘
     │  │            0x724BCCE3                   │                   │
     │  │              ┏━┷━┓                      │                   │
     └──┼──────────────┨XOR┃                      │                   │
     ┌──┘              ┗━┯━┛                      │                   │
     L2                  R2                       X                   X
 0x5E1CEC63          0x82E13C49
     └───────┐       ┌───┘
        0x82E13C495E1CEC63
  ┏━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┓
  ┃ Inverse Initial Permutation ┃
  ┗━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┛
                 │
            Ciphertext
        0x13C2ACADA41E9B58
```
