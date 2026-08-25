# aavbase.dat — Análisis (con dump de memoria)

## Resumen ejecutivo

**Es una base de datos cifrada, no falsa.** Contiene **67 firmas reales** de malware (2003-2005), insuficiente para tests de 2006 con 147k+ muestras nuevas. Eso explica el 0%.

## Datos duros

- **Tamaño:** 15141 B (header 22 B `Abacre Antivirus Bases` + payload 15119 B)
- **SHA256:** `21384F028AC1CC7330361FFD084E7A1EA2FFB8B215ECB48BE629E7E5D0980F33`
- **Entropía payload:** 7.9876 bits/byte → cifrado de flujo confirmado
- **Funciones:** `LoadVirBase:` @0x2266EA, `UnLoadVirBase:` @0x2267B4 (Delphi)

## Hipótesis Blowfish (no verificada al100%)

Se encontraron strings `Cipher_Blowfish` en memoria (`0x21F3CF`), `Blowfish=` en config (`0x5290CE`) y una key candidata (`0x2266A2`). Sin embargo:

**Lo que sabemos:**
- El string `Cipher_Blowfish` aparece en la clase Delphi del cifrador
- La key está en la dirección `0x2266A2`
- La entropía del payload (7.9876) es consistente con Blowfish CBC

**Lo que NO sabemos:**
- No se realizó descifrado real del payload — el plaintext no se obtuvo
- Las comillas en la key (`dkmoaio"jof"...`) podrían ser artefactos del dump
- El payload (15119 B) **no es múltiplo de 8** (resto 7), lo cual es problemático para Blowfish CBC puro

**Posibles explicaciones del payload no-múltiplo-de-8:**
1. Blowfish en modo CTR (no requiere padding)
2. Header adicional de 7 bytes dentro del payload
3. Error en la medición del dump
4. Cifrador diferente (no Blowfish, pese a los strings)

> **Conclusión:** Blowfish es la hipótesis más probable pero no demostrada. Falta el descifrado offline para confirmarlo.

## Firmas extraídas del dump (67)

Extraídas de memoria desempaquetada `aav_fulldump.dmp` (29 MB, `ntsd -pv`):

```
W32.Beagle.W@mm, W32.Beagle.X@mm, W32.Blaster.T.Worm, W32.Bugbear.C/E,
W32.Dumaru.AI, W32.Gaobot.* (YC,WO,WX,ADN,AAY,ADV...), W32.Netsky.* (B,S,T,U,V,W,X,Y,Z,AA,AB,AC),
W32.Sasser.B/C/D, W32.Lovgate.R, W32.Mydoom.I/J, Trojan.Mitglieder.F/H/I/J, Trojan.AphexLace.Kit...
```

Lista completa en `analysis/aavbase/signatures.txt`

Todas son gusanos/trojans de 2003-2005. Ningún malware post-2005 → 0% en tests con 147k muestras modernas.

## Formato reconstruido (parcial)

```
[Header 22B] "Abacre Antivirus Bases"
[Payload cifrado]
  -> plaintext esperado:
    [NumFirmas: 4B LE]
    [Registro: Longitud Firma | Nombre null-terminated | Hash/Raw pattern]
```

**Pendiente:** Descifrado offline exacto para confirmar estructura.

## Lo que se desconoce (limitaciones de la investigación)

### Motor de escaneo
No se analizó cómo Abacre compara firmas contra archivos. Posibilidades:
- Hash MD5/CRC32 del archivo completo
- Patrón de bytes (byte-signature matching)
- Hash de secciones PE

Sin el descifrado del payload, no se puede determinar qué tipo de patrón almacena cada firma.

### Motor heurístico
No se encontró evidencia de heurísticas funcionales. Las pruebas de virus.gr incluían sección de heurísticas y Abacre no aparecía — lo que sugiere que **nunca tuvo motor heurístico funcional**, solo matching de firmas contra `aavbase.dat`.

### aavshield.exe (resident shield)
No se analizó en profundidad. Se desconoce:
- Mecanismo de hooking (¿API hooking? ¿Driver? ¿Polling?)
- Cómo intercepta apertura de archivos
- Si comparte la misma base de firmas

### Conexiones de red
No se analizó si Abacre intentaba conexiones de red (telemetría, actualizaciones fallidas, etc.).

### Packer
No se identificó el packer específico (no es UPX, ASPack ni PECompact conocido). El análisis se limitó a detectar packing por entropía y secciones vacías, sin unpack manual.

## Contexto: producto abandonado, no engaño

Es importante matizar: Abacre no era un "antivirus falso" — era un producto **abandonado por su vendor**. La empresa Abacre se dedica a software POS (punto de venta) y el antivirus parece haber sido un experimento de diversificación que nunca recibió actualizaciones. El 0% es resultado de negligencia comercial, no de intención fraudulenta.

## Conclusión

> *Tener 67 firmas cifradas no es "fake", es "obsoleto". En 2006 competidores tenían 100k+ firmas + heurísticas. Abacre solo tenía patterns de 2003-2005 sin motor heurístico.*

Ver `analysis/aavbase/aav_fulldump.dmp` (29 MB) para reproducir.
