# Guía completa — Procedimiento en VM (3ª persona)

> **Objetivo:** Obtener la memoria desempaquetada de `aav.exe` y el plaintext de `aavbase.dat` sin exponer el host.

---

## Estado inicial

El repositorio ya contiene:
```
original/setup.exe
extracted/app/aav.exe, aavshield.exe, aavbase.dat (15 KB)
tools/x64dbg/release/x32/x32dbg.exe    ← No compatible con XP
tools/vc_redist/vc_redist.x86.exe       ← Fix para error DLL en Win7
tools/x64dbg_xp/olly110/OLLYDBG.EXE    ← OllyDbg 1.10 (XP compatible)
```

---

## Paso 1 — Creación de la máquina virtual

Se recomienda **VMWare Workstation Pro 26H1** (VirtualBox presentó problemas de rendimiento e Hyper-V invirtió el cursor). Se crea una VM con:

| Parámetro | Valor |
|-----------|-------|
| SO | Windows XP Professional SP3 (32 bits) |
| RAM | 2048 MB |
| Disco | 20 GB |
| Red | Deshabilitada (aislamiento total) |

Tras instalar el sistema, se toma una **instantánea** denominada `limpio`.

**Nota:** Abacre **no es compatible con Windows 7** — el asistente de compatibilidad bloquea la ejecución. Solo funciona en XP.

---

## Paso 2 — Transferencia de archivos

Mediante **VMWare Tools** se comparte la carpeta del proyecto y se copia al disco local de la VM:
```cmd
xcopy /E /I \\vmware-host\Compartida\* C:\Abacre\
```

Contenido de `C:\Abacre\`:
```
aav.exe              ← Antivirus principal
aavshield.exe        ← Resident shield
aavbase.dat          ← Base cifrada Blowfish
setup.exe            ← Instalador original
tools\               ← Herramientas de análisis
scripts\             ← Scripts reproducibles
```

**Error DLL:** Si x32dbg falla con `api-ms-win-crt-runtime-l1-1-0.dll`, se instala `vc_redist.x86.exe` dentro de la VM y se reinicia. En XP, x32dbg 2026 **no es compatible** — se usa OllyDbg 1.10 o ntsd.

---

## Paso 3 — Apertura con depurador

### Opción A: OllyDbg 1.10 (recomendada para XP)

Se abre `C:\tools\x64dbg_xp\olly110\OLLYDBG.EXE`. Mediante `File → Open` se carga `C:\Abacre\aav.exe`.

En la barra de comandos inferior se establece:
```
bp LoadLibraryA
bp GetProcAddress
```

Se presiona `F9` de forma reiterada (aproximadamente 20-30 veces) hasta observar el salto `JMP 0x4xxxxx` y código legible `PUSH EBP`. La ventana superior debe indicar `module aav` y `EIP = 0040xxxx` en lugar de `kernel32`.

> **Advertencia:** El packer de Abacre detecta OllyDbg y lanza **Error 251** (`Protection Error: Debugger detected!`). Si esto ocurre, usar el método alternativo (Paso 3B).

### Opción B: NTSD — attach no invasivo (recomendado)

Dado que el packer posee detección de debugger, se ejecuta `aav.exe` de forma normal fuera del depurador y se realiza attach:

1. Se abre `aav.exe` con doble clic (se visualiza la GUI de Abacre).
2. En el **Administrador de tareas** se anota el PID (columna PID activada).
3. En `CMD` se ejecuta:
```cmd
ntsd -pv -p <PID>
.dump aav.dmp
.dump /f aav_fulldump.dmp
q
```

El modificador `-pv` realiza attach no invasivo — el packer **no detecta** el debugger.

> **Error 123:** Si se escribe `.dump /ma a:\ruta\aav.dmp` con una ruta, NTSD interpreta el espacio como separador. **Solución:** escribir sin ruta — el dump queda en `C:\Documents and Settings\Usuario\`.

Los dumps quedan en `C:\Documents and Settings\Usuario\` (mini 11 KB, full ~29 MB) y se copian a `analysis/aavbase/`.

---

## Paso 4 — Volcado de memoria (método Scylla)

Si se usa OllyDbg sin que el packer detecte, se accede a `Plugins → Scylla → Dump + Fix`:

1. `IAT Autosearch` → detecta la tabla de imports
2. `Get Imports` → resuelve las funciones importadas
3. `Dump` → genera `aav_dump.exe`
4. `Fix Dump` → genera `aav_dump_fixed.exe` con imports corregidos

Sin plugin Scylla, se utiliza `View → Memory (ALT+M)` o `Copy to executable → Selection`.

---

## Paso 5 — Extracción del plaintext

Se reinicia el depurador con `aav_dump_fixed.exe`. Se establece `bp CreateFileA` y se ejecuta. Cuando `lpFileName` corresponde a `aavbase.dat`, se ingresa con `F7` hasta el bucle de descifrado (contador `0x3B0F` = 15119). Tras la llamada, el registro `EDI` apunta al buffer descifrado, el cual se guarda mediante `Backup → Save Data` como `aavbase_plain.bin`.

---

## Paso 6 — Retorno al host

Los archivos `aav_dump_fixed.exe` y `aav_fulldump.dmp` se copian al host en `analysis/aavbase/`. La VM se revierte a la instantánea `limpio`. El análisis de firmas se realiza con `scripts/03_statistical_crypto.py` y la lista se encuentra en `analysis/aavbase/signatures.txt`.

---

## Scripts de análisis

```powershell
python scripts\01_analyze_aavbase.py          # SHA256, hex, entropía
python scripts\03_statistical_crypto.py        # Frecuencia, autocorrelación
python scripts\04_find_decrypt.py              # Buscar rutina de descifrado
python scripts\06_extract_signatures.py        # Extraer firmas del dump
.\scripts\run_all.ps1                          # Ejecutar todo
```

---

## Tabla de errores comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| x32dbg: DLL faltante en Win7 | Falta `api-ms-win-crt-runtime-l1-1-0.dll` | Instalar `vc_redist.x86.exe` |
| x32dbg: "no es Win32 válida" en XP | x64dbg 2026 incompatible con XP | Usar OllyDbg 1.10 o ntsd |
| OllyDbg → Error 251 | Packer detecta debugger | Usar `ntsd -pv` |
| procdump → Acceso denegado | No es Win32 válido en XP | Usar `ntsd -pv` |
| Error 123 al hacer dump | Ruta con espacios interpretada como argumento | Escribir sin ruta |
| Windows 7 bloquea aav.exe | Incompatibilidad de SO | Usar XP SP3 |
| Dump mini = 11 KB | `.dump` sin `/f` solo guarda headers | Usar `.dump /f` |

---

## Notas

- Windows 7 no resultó compatible con Abacre; se requiere XP SP3.
- VirtualBox e Hyper-V fueron descartados por rendimiento y detección de mouse.
- El packer detecta breakpoints por software; el método `ntsd -pv` resulta más estable que Olly con breakpoints.
- La key Blowfish está en `0x2266A2` del dump y la clase `Cipher_Blowfish` en `0x21F3CF`.
