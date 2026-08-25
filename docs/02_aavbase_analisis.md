# aavbase.dat — Análisis (con dump de memoria)

## Resumen ejecutivo

**Es una base de datos cifrada, no falsa.** Contiene **67 firmas reales** de malware (2003-2005). La evidencia disponible sugiere que esta cobertura extremadamente limitada constituye una explicación plausible para su 0,00% de detección en las pruebas de Virus.gr, aunque no se puede demostrar causalidad sin el conjunto completo de muestras.

## Datos duros

- **Tamaño:** 15141 B (header 22 B `Abacre Antivirus Bases` + payload 15119 B)
- **SHA256:** `21384F028AC1CC7330361FFD084E7A1EA2FFB8B215ECB48BE629E7E5D0980F33`
- **Entropía payload:** 7.9876 bits/byte → distribución compatible con datos cifrados o fuertemente ofuscados
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

Todas son gusanos/trojans identificables de 2003-2005. No se encontró malware post-2005 en la base.

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
No se encontró evidencia suficiente de un motor heurístico funcional. La ausencia de Abacre en la tabla de detección exclusivamente heurística de Virus.gr es un indicio adicional, pero no constituye prueba de inexistencia.

### aavshield.exe (resident shield)
No se analizó en profundidad. Se desconoce:
- Mecanismo de hooking (¿API hooking? ¿Driver? ¿Polling?)
- Cómo intercepta apertura de archivos
- Si comparte la misma base de firmas

### Conexiones de red
No se analizó si Abacre intentaba conexiones de red (telemetría, actualizaciones fallidas, etc.).

### Packer
No se identificó el packer específico (no es UPX, ASPack ni PECompact conocido). El análisis se limitó a detectar packing por entropía y secciones vacías, sin unpack manual.

## Contexto

La evidencia analizada no permite determinar las razones comerciales o técnicas por las que la base dejó de actualizarse. No se ha encontrado evidencia en esta investigación que permita afirmar que Abacre fuera deliberadamente fraudulento.

## Arquitectura reconstruida

```
                    ┌────────────────────┐
                    │     aav.exe        │
                    │  Motor principal   │
                    │  (Delphi, packed)  │
                    └─────────┬──────────┘
                              │
                 ┌────────────┴─────────────┐
                 │                          │
          LoadVirBase()               Scanner
          [confirmado]              [desconocido]
                 │                          │
                 ▼                          │
          aavbase.dat                       │
          [15 KB, cifrado]                  │
                 │                          │
          Blowfish [?]                      │
          [hipótesis]                       │
                 │                          │
                 ▼                          ▼
          Signature DB ───────────────> Detección
          [67 firmas]                [sin heurísticas
          [2003-2005]                 evidenciadas]

                    ┌────────────────────┐
                    │  aavshield.exe     │
                    │ Protección residente│
                    │ [no analizado]     │
                    └────────────────────┘
```

**Leyenda:**
- 🟢 **Confirmado:** LoadVirBase, 67 firmas, estructura PE, packing
- 🟡 **Inferido:** Blowfish (strings encontrados, sin descifrado), formato de registros
- 🔴 **Desconocido:** Motor de escaneo, heurísticas, aavshield.exe, packer específico

## Conclusión

> *La evidencia sugiere que 67 firmas de 2003-2005 era una cobertura extremadamente limitada para una prueba de 2006 con 147k muestras. Sin embargo, no se puede establecer causalidad directa sin el conjunto completo de muestras de Virus.gr.*

Ver `analysis/aavbase/aav_fulldump.dmp` (29 MB) para reproducir.
