# Guía Simple — Procedimiento en VM (3ª persona)

> **Objetivo:** Obtener la memoria desempaquetada de `aav.exe` y el plaintext de `aavbase.dat` sin exponer el host.

## Estado inicial
El repositorio ya contiene:
```
original/setup.exe
extracted/app/aav.exe, aavshield.exe, aavbase.dat (15 KB)
tools/x64dbg/release/x32/x32dbg.exe
tools/vc_redist/vc_redist.x86.exe
tools/x64dbg_xp/olly110/OLLYDBG.EXE (alternativa XP)
```

## Paso 1 — Creación de la máquina virtual
Se recomienda VMWare Workstation Pro 26H1 (VirtualBox presentó problemas de rendimiento y Hyper-V invirtió el cursor). Se crea una VM con Windows XP Professional SP3 de 32 bits, 2048 MB de RAM, 20 GB de disco y red deshabilitada. Tras instalar el sistema, se toma una instantánea denominada `limpio`.

## Paso 2 — Transferencia de archivos
Mediante VMWare Tools se comparte la carpeta del proyecto y se copia al disco local de la VM `C:\Abacre\`:
- `aav.exe`, `aavbase.dat`, `aavshield.exe`
- `tools/x64dbg/release` → `C:\tools\x64dbg\`
En caso de error `api-ms-win-crt-runtime` se instala `vc_redist.x86.exe` dentro de la VM y se reinicia. Para XP se utiliza `OLLYDBG.EXE` en lugar de `x32dbg` (snapshot 2026 no es Win32 válido en XP).

## Paso 3 — Apertura con depurador
Se abre `C:\tools\x64dbg\release\x32\x32dbg.exe` (o `OLLYDBG.EXE` en XP). Mediante `File → Open` se carga `C:\Abacre\aav.exe`. En la barra de comandos inferior se establece:
```
bp LoadLibraryA
bp GetProcAddress
```
Se presiona `F9` de forma reiterada (aproximadamente 20-30 veces) hasta observar el salto `JMP 0x4xxxxx` y código legible `PUSH EBP`. La ventana superior debe indicar `module aav` y `EIP = 0040xxxx` en lugar de `kernel32`.

## Paso 4 — Volcado de memoria
Sin cerrar el depurador, se accede a `Plugins → Scylla → Dump + Fix`:
- `IAT Autosearch` → `Get Imports` → `Dump` → `aav_dump.exe`
- `Fix Dump` → `aav_dump_fixed.exe`
En Olly sin plugin se utiliza `View → Memory (ALT+M)` o `Copy to executable → Selection`, o bien el método no invasivo descrito en el paso alternativo.

### Método alternativo no invasivo (recomendado para XP)
Dado que el packer posee detección de debugger (Error 251, `Debugger detection!`), se ejecuta `aav.exe` de forma normal fuera del depurador y se realiza attach:
1. Se abre `aav.exe` con doble clic (se visualiza la GUI de Abacre).
2. En el Administrador de tareas se anota el PID (columna PID activada).
3. En `CMD` se ejecuta:
```
ntsd -pv -p <PID>
.dump aav.dmp
.dump /f aav_fulldump.dmp
q
```
El modificador `-pv` realiza attach no invasivo. La ruta sin directorio evita el error 123 (`a:Abacre`). Los dumps quedan en `C:\Documents and Settings\Usuario\` (mini 11 KB, full ~29 MB) y se copian a `analysis/aavbase/`.

## Paso 5 — Extracción del plaintext
Se reinicia el depurador con `aav_dump_fixed.exe`. Se establece `bp CreateFileA` y se ejecuta. Cuando `lpFileName` corresponde a `aavbase.dat`, se ingresa con `F7` hasta el bucle de descifrado (contador `0x3B0F` = 15119). Tras la llamada, el registro `EDI` apunta al buffer descifrado, el cual se guarda mediante `Backup → Save Data` como `aavbase_plain.bin`.

## Paso 6 — Retorno al host
Los archivos `aav_dump_fixed.exe` y `aav_fulldump.dmp` se copian al host en `analysis/aavbase/`. La VM se revierte a la instantánea `limpio`. El análisis de firmas se realiza con `scripts/03_statistical_crypto.py` y la lista se encuentra en `analysis/aavbase/signatures.txt`.

## Notas
- Windows 7 no resultó compatible con Abacre; se requiere XP SP3.
- VirtualBox e Hyper-V fueron descartados por rendimiento y detección de mouse.
- El packer detecta breakpoints por software; el método `ntsd -pv` resulta más estable que Olly con breakpoints.
