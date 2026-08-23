import pathlib, re, pefile, collections
exe = pathlib.Path(r"C:\Users\Usuario\Documents\Visual Studio 2022\Projects\Abacre_Inv\_extracted\app\aav.exe")
b = exe.read_bytes()
print("Buscando quien descifra aavbase.dat...")
# strings que cargan el archivo
for kw in [b"aavbase", b"Abacre Antivirus Bases", b"BaseVer", b"aavversion"]:
    idx=b.find(kw)
    print(f" {kw.decode()} @ {hex(idx) if idx!=-1 else 'NO'}")
# buscar CreateFile/ReadFile resueltos via GetProcAddress - buscar nombres en binario
for api in [b"CreateFileA", b"ReadFile", b"Crypt", b"RC4", b"AES"]:
    print(f" {api.decode()} {'FOUND' if api in b else 'no'}")
# buscar constantes RC4 S-box 0..255 o AES S-box
if bytes(range(256)) in b:
    print(" S-box RC4 identica encontrada")
else:
    print(" S-box no literal (generada en runtime)")
# PE imports dinamicos
pe=pefile.PE(str(exe))
print(f"EP 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X} -> stub packing, OEP real oculto")
print("Siguiente paso OBLIGATORIO: VM aislada + x64dbg")
print(" 1. bp LoadLibraryA / GetProcAddress")
print(" 2. trace hasta OEP (tipico: pushad, mov esi, ...)")
print(" 3. Scylla dump + fix imports")
print(" 4. IDR sobre dump -> buscar TfrmMain.ScanFile / LoadBases")
print(" 5. breakpoint en CreateFileA('aavbase.dat') -> seguir descifrado -> dump plaintext")
