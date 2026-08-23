# Metodología — Abacre Antivirus RE

## Fase 1 — Extracción estática (completada)
- Identificar wrapper: Inno Setup 5.1.2 (PE 8 secciones, entropía 7.98)
- Extraer con `innoextract 1.9` → 8 archivos en `extracted/app`

## Fase 2 — Triage PE (completada)
- PE 32-bit, 11 secciones vacías, EP 0x1000, timestamp falso 1992, VersionInfo vacío
- Imports minimizados → packing agresivo
- Recursos Delphi `DVCLAL/PACKAGEINFO/TFRM*` cifrados

## Fase 3 — aavbase.dat (completada)
- 15 KB, entropía 7.9876, sin strings Unicode, sin compresión estándar, flujo cifrado
- Ver `analysis/aavbase/statistical.txt`

## Fase 4 — Desempaquetado dinámico (pendiente VM)
```
aav.exe packed
  -> LoadLibraryA / GetProcAddress (reconstruye imports)
  -> OEP real
  -> CreateFileA("aavbase.dat") -> función descifrado -> plaintext
```
Herramientas: x64dbg + Scylla + IDR + PE-bear + Procmon

## Fase 5 — Reconstrucción formato
Objetivo: [ID][Nombre][Longitud][Firma] o [Hash][Tipo][Acción]
