import argparse
import sys
from chacha20_poly1305 import chacha20_poly1305

REVERSE = "reverse"
ENCRYPT = "encrypt"


if __name__ == "__main__":
	encrypted = chacha20_poly1305("portelaselada", "Pedro Renato Mariano de Figueiredo Gonçalves", ENCRYPT)
	print(encrypted)
	decrypted = chacha20_poly1305("portelaselada", encrypted, REVERSE)
	print(decrypted)