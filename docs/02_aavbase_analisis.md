# aavbase.dat — Análisis Detallado

- **Tamaño:** 15141 B (payload 15119 B)
- **SHA256:** 21384F028AC1CC7330361FFD084E7A1EA2FFB8B215ECB48BE629E7E5D0980F33
- **Cabecera:** `Abacre Antivirus Bases` (22 B, entropía 3.69)
- **Entropía payload:** 7.9876 bits/byte (>7.5 = cifrado)
- **Strings ASCII:** solo cabecera + fragmentos 4-6 chars aleatorios
- **Unicode:** 0
- **Compresión:** zlib/bz2/lzma FAIL
- **Distribución:** 256/256 bytes, chi2 258, 0 bloques repetidos → stream cipher (RC4/AES-CTR)
- **Ventanas:** 256B avg 7.16 → 2048B avg 7.91 (uniforme)

No conclusión "DB falsa" sin descifrar. Tamaño permite ~900 firmas de 16B.
Pendiente: identificar función descifrado en dump desempaquetado.
