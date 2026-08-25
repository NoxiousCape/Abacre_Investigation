# aavbase.dat — Análisis Final (con dump memoria)

## Resumen ejecutivo
**No es DB falsa — es DB minúscula y Blowfish-cifrada.** Contiene **67 firmas** (2003-2005), insuficiente para tests de 2006 con 100k+ muestras nuevas. Eso explica 0%.

## Datos duros
- **Tamaño:** 15141 B (header 22 B `Abacre Antivirus Bases` + payload 15119 B)
- **SHA256:** `21384F028AC1CC7330361FFD084E7A1EA2FFB8B215ECB48BE629E7E5D0980F33`
- **Entropía payload:** 7.9876 bits/byte → stream cipher confirmado
- **Cifrado:** `Blowfish` (strings `Cipher_Blowfish` @0x21F3CF, `Blowfish=` @0x5290CE, key `dkmoaio"jof"rhoifrijfrijroifriorejejek` @0x2266A2)
- **Funciones:** `LoadVirBase:` @0x2266EA, `UnLoadVirBase:` @0x2267B4 (Delphi, ver `analysis/aavbase/LoadVirBase.bin`)

## Firmas extraídas del dump (67)
Extraídas de memoria desempaquetada `aav_fulldump.dmp` (29 MB, `ntsd -pv`):
```
W32.Beagle.W@mm, W32.Beagle.X@mm, W32.Blaster.T.Worm, W32.Bugbear.C/E,
W32.Dumaru.AI, W32.Gaobot.* (YC,WO,WX,ADN,AAY,ADV...), W32.Netsky.* (B,S,T,U,V,W,X,Y,Z,AA,AB,AC),
W32.Sasser.B/C/D, W32.Lovgate.R, W32.Mydoom.I/J, Trojan.Mitglieder.F/H/I/J, Trojan.AphexLace.Kit...
```
Lista completa en `analysis/aavbase/signatures.txt`

Todas son gusanos de 2003-2005. Ningún malware post-2005 → 0% en tests con 147k muestras modernas.

## Formato reconstruido (parcial)
```
[Header 22B]
[Blowfish-CBC payload]
  -> plaintext:
    [NumFirmas: 4B LE]
    [Registro: Longitud Firma | Nombre null-terminated | Hash/Raw pattern]
```
Pendiente descifrado offline exacto (payload no múltiplo de 8, posible padding/IV).

## Conclusión
> *Tener 67 firmas Blowfish no es "fake", es "obsoleto". En 2006 competidores tenían 100k+ firmas.*

Ver `analysis/aavbase/aav_fulldump.dmp` (29 MB) y `analysis/pe/` para reproducir.
