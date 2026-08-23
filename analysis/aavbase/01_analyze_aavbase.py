import pathlib, hashlib, math, re, collections, struct
p = pathlib.Path(r"C:\Users\Usuario\Documents\Visual Studio 2022\Projects\Abacre_Inv\_extracted\app\aavbase.dat")
b = p.read_bytes()
size = len(b)
sha = hashlib.sha256(b).hexdigest()
print("TAMANO:", size, "bytes (14.79 KB)")
print("SHA256:", sha)
hdr = b[:22]
print("Header:", hdr)
hx = " ".join(f"{c:02X}" for c in hdr)
print("Header hex:", hx)
print("Rest size:", size-22)
print("--- PRIMEROS 256 BYTES ---")
for i in range(0,256,16):
    chunk = b[i:i+16]
    hexs = " ".join(f"{c:02X}" for c in chunk)
    asc = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
    print(f"{i:04X}: {hexs:<48} |{asc}|")
strs_ascii = re.findall(rb"[\x20-\x7E]{4,}", b)
print("--- STRINGS ASCII ---", len(strs_ascii))
for s in strs_ascii:
    print(s.decode())
strs_uni = re.findall(rb"(?:[\x20-\x7E]\x00){4,}", b)
print("--- STRINGS UNICODE ---", len(strs_uni))
decoded = [s.decode("utf-16le") for s in strs_uni]
print(decoded[:5] if decoded else "(ninguna)")
def entropy(data):
    if not data: return 0
    freq = collections.Counter(data)
    return -sum((v/len(data))*math.log2(v/len(data)) for v in freq.values())
print("--- ENTROPIA ---")
print(f"Total: {entropy(b):.4f} bits/byte")
print(f"Header 22B: {entropy(b[:22]):.4f}")
print(f"Payload {size-22}B: {entropy(b[22:]):.4f}")
cnt = collections.Counter(b[22:])
print("Bytes unicos payload:", len(cnt), "/256")
print("Top5:", cnt.most_common(5))
import zlib, bz2, lzma
for name, fn in [("zlib", zlib.decompress), ("bz2", bz2.decompress), ("lzma", lzma.decompress)]:
    try:
        dec = fn(b[22:])
        print(name, "OK", len(dec))
    except Exception as e:
        print(name, "FAIL", str(e)[:80])
print("--- XOR single byte brute ---")
found=False
for k in range(256):
    dec = bytes(c ^ k for c in b[22:122])
    printable = sum(1 for c in dec if 32 <= c <= 126 or c in (10,13))
    if printable > 70:
        print(f"key {k:02X} {dec[:70]}")
        found=True
if not found:
    print("(ninguna clave >70% printable)")
print("--- LE32 view ---")
for i in range(0,32,4):
    v = struct.unpack_from("<I", b, 22+i)[0]
    be = struct.unpack_from(">I", b, 22+i)[0]
    print(f" +{i:02d} LE={v} BE={be}")
