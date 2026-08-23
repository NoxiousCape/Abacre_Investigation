import pathlib, hashlib, math, re, collections, pefile
for name in ["aav.exe","aavshield.exe"]:
    p = pathlib.Path(f"C:/Users/Usuario/Documents/Visual Studio 2022/Projects/Abacre_Inv/_extracted/app/{name}")
    b = p.read_bytes()
    sha = hashlib.sha256(b).hexdigest()
    print(f"=== {name} ===")
    print(f"Tamano: {len(b)} bytes ({len(b)/1024:.1f} KB) SHA256: {sha}")
    pe = pefile.PE(str(p))
    print(f" EP RVA 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X} ImageBase 0x{pe.OPTIONAL_HEADER.ImageBase:X}")
    print(f" Secciones: {len(pe.sections)} ")
    for i,s in enumerate(pe.sections):
        data=s.get_data()
        ent = 0
        if len(data)>0:
            c=collections.Counter(data)
            ent=-sum((v/len(data))*math.log2(v/len(data)) for v in c.values())
        print(f"  {i}: Name={s.Name!r} VA=0x{s.VirtualAddress:06X} VS=0x{s.Misc_VirtualSize:05X} Raw={len(data)} Ent={ent:.3f}")
    if hasattr(pe,"DIRECTORY_ENTRY_IMPORT"):
        print(" Imports:")
        for e in pe.DIRECTORY_ENTRY_IMPORT:
            print(f"  {e.dll.decode()} -> {[imp.name.decode() if imp.name else str(imp.ordinal) for imp in e.imports[:8]]}")
    else:
        print(" Imports: NINGUNO (packed)")
    ep_off = pe.get_offset_from_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    print(f" EP bytes: {b[ep_off:ep_off+32].hex(' ')}")
    # resources
    if hasattr(pe,"DIRECTORY_ENTRY_RESOURCE"):
        print(f" Recursos: {len(list(pe.DIRECTORY_ENTRY_RESOURCE.entries))} tipos")
        for e in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if e.id==10:
                print("  RT_RCDATA (Delphi forms):")
                for sub in e.directory.entries[:5]:
                    nm = sub.name.string.decode() if sub.name else str(sub.id)
                    sz = sub.directory.entries[0].data.struct.Size
                    print(f"   {nm} {sz}B")
    print()

# intentar desempaquetado simple: buscar firma unpack stub
import pathlib
for name in ["aavshield.exe"]:
    b = pathlib.Path(f"C:/Users/Usuario/Documents/Visual Studio 2022/Projects/Abacre_Inv/_extracted/app/{name}").read_bytes()
    # buscar patrones ASPack
    if b"aPLib" in b: print("aPLib found -> ASPack")
    if b"UPX" in b: print("UPX found")
    if b"ASPack" in b: print("ASPack string")
    # strings relevantes
    strs = re.findall(rb"[\x20-\x7E]{4,}", b)
    print("Strings legibles totales:", len(strs))
    longs = [s.decode() for s in strs if len(s)>6]
    print(longs[:10])
