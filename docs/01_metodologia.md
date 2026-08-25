# Metodología

## Fase 1 — Extracción estática
Se identifica el wrapper Inno Setup 5.1.2 (PE 8 secciones, entropía 7.98). La extracción se realiza con `innoextract 1.9` hacia `extracted/app`.

## Fase 2 — Triage PE
Se analiza el binario de 32 bits: 11 secciones vacías, EP 0x1000, timestamp falsificado 1992, VersionInfo vacío e imports minimizados. Los recursos Delphi `DVCLAL/PACKAGEINFO/TFRM*` se encuentran cifrados, por lo que se requiere desempaquetado dinámico.

## Fase 3 — Análisis de aavbase.dat
El archivo presenta 15 KB con entropía 7.9876, sin strings Unicode ni compresión estándar. El análisis estadístico revela flujo cifrado (distribución uniforme, 0 bloques repetidos), posteriormente identificado como Blowfish mediante dump de memoria.

## Fase 4 — Desempaquetado dinámico
El binario empaquetado reconstruye imports mediante `LoadLibraryA/GetProcAddress` hasta alcanzar el OEP. El procedimiento se ejecuta en VM aislada con `ntsd -pv` y `OllyDbg`, generando `aav_fulldump.dmp` (29 MB). El detalle se encuentra en `docs/04_guia_vm_completa.md`.

## Fase 5 — Reconstrucción
A partir del dump se extraen `LoadVirBase` @0x2266EA y 67 firmas (W32.Netsky, Gaobot, etc.), lo que permite inferir el formato `[Header][Blowfish-CBC payload]` → `[NumFirmas][Registros]`.
