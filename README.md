# Abacre Antivirus 1.3 — Ingeniería Inversa Académica

> **Fines exclusivamente académicos y de investigación.** Análisis estático de un antivirus histórico (2006) que obtuvo 0% de detección en pruebas independientes.

## Contexto
Abacre Antivirus v1.3 (Inno Setup 5.1.2) es objeto de estudio para comprender las causas de su fallo en evaluaciones de 113.334 y 58 productos. El binario se encuentra desarrollado en Delphi, empaquetado y con base de firmas cifrada mediante Blowfish.

## Estructura
```
original/          # Instalador original y hashes SHA256
extracted/app/     # Payload extraído con innoextract 1.9
  aav.exe          # GUI principal (Delphi packed)
  aavshield.exe    # Resident shield (packed)
  aavbase.dat      # Base de firmas Blowfish (15 KB, 70 firmas)
Screenshots/       # Evidencias VM (1.png-10.png)
docs/              # Informes técnicos y guías
  proceso_vm/      # Proceso documentado paso a paso
analysis/          # hashes, entropía, dumps, firmas
  aavbase/         # aav_fulldump.dmp (29 MB), signatures.txt
scripts/           # Scripts forense reproducibles
tools/             # innoextract, x64dbg, vc_redist, procdump
```

## Hallazgos
- **Installer:** Inno Setup 5.1.2, `SHA256 7EB44CC2...` (1362759 B)
- **Packing:** 11 secciones vacías, entropía 7.99, imports mínimos `LoadLibraryA/GetProcAddress` — se requiere desempaquetado dinámico
- **aavbase.dat:** 15141 B, entropía 7.9876, 256/256 bytes uniformes, cifrado Blowfish (key `dkmoaio"jof"...` @0x2266A2, `Cipher_Blowfish` @0x21F3CF), 70 firmas reales (W32.Netsky, Gaobot, Beagle 2003-2005) — explica 0% frente a malware posterior
- **Desempaquetado:** Realizado en VMWare Workstation Pro 26H1 + XP SP3 mediante `ntsd -pv` → `aav_fulldump.dmp` (29 MB) — ver `docs/proceso_vm/README.md`

## Reproducción
```powershell
# 1. Extracción
tools\innoextract.exe --extract --output-dir extracted original\setup.exe
# 2. Análisis estático
python scripts\01_analyze_aavbase.py
python scripts\03_statistical_crypto.py
# 3. Análisis dinámico (VM aislada, sin red)
# Ver docs/04_guia_vm_completa.md
```

## Créditos proceso VM
El procedimiento de dump fue documentado por el investigador en VMWare Workstation Pro 26H1 con XP SP3 (VirtualBox/Hyper-V descartados por rendimiento). La secuencia completa se encuentra en `Screenshots/` y `docs/proceso_vm/`.

## Disclaimer
Los binarios no deben ejecutarse en el host. Se requiere VM aislada sin red. Se respeta la licencia original de Abacre.
