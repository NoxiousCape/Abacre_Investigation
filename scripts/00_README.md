# Abacre Antivirus - Scripts Forense
# Fecha: 2026-08-22
# Workspace: Abacre_Inv

## Objetivo
Investigar quien descifra aavbase.dat y reconstruir estructura:
aavbase.dat -> funcion descifrado (aav.exe) -> plaintext -> firmas

## Scripts
01_analyze_aavbase.py       - Tamano, SHA256, hex, entropy, strings
02_analyze_aavshield.py     - PE packing, imports, EP
03_statistical_crypto.py    - Frecuencia, entropia ventanas, autocorrelacion, pares
04_find_decrypt.py          - Busca rutina descifrado en aav.exe (RC4/AES/XOR const)
05_dump_attempt.py          - Intento dump payload .data

## Uso
python scripts_forense\03_statistical_crypto.py
python scripts_forense\04_find_decrypt.py
