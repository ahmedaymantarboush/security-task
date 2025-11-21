from .technique import Technique
import os
import base64


class AESCipher(Technique):
    """
    Implementation of the Advanced Encryption Standard (AES) algorithm.
    Supports 128, 192, and 256-bit keys in CBC (Cipher Block Chaining) mode.
    """
    
    # AES S-box (Substitution Box) used for SubBytes step
    # It provides non-linearity to the cipher.
    S_BOX = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]

    # AES Inverse S-box used for decryption
    INV_S_BOX = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    ]

    # Round constants for Key Expansion
    RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
    
    # Multiplication matrices for MixColumns (False for Encrypt, True for Decrypt)
    MUL = {False: ([2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]), True: ([14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14])}

    def __init__(self, key=None, key_size=None):
        self._initial_key, self._initial_key_size = key, key_size
        self.key = self.key_size = self.key_length = self.num_rounds = self.round_keys = None
        self._key_initialized = False
    
    def _ensure_key_initialized(self):
        """Initialize key and round keys if not already done."""
        if self._key_initialized:
            return
        
        # Use provided key_size or default to 128
        ks = self._initial_key_size if self._initial_key_size else 128
        
        # Use provided key or generate random
        k = self._initial_key
        
        # Set key length (bytes) and number of rounds based on key size (bits)
        self.key_size, self.key_length, self.num_rounds = ks, ks//8, {128:10,192:12,256:14}[ks]
        
        # Generate key: random if None, otherwise encode/pad to correct length
        if k is None:
            self.key = os.urandom(self.key_length)
        else:
            # Handle string keys by encoding
            if isinstance(k, str):
                k = k.encode()
            # Pad or truncate to correct length
            if len(k) < self.key_length:
                k = k + b'\0' * (self.key_length - len(k))
            self.key = k[:self.key_length]
        
        # Expand the key into round keys
        self.round_keys = self.key_expansion()
        self._key_initialized = True
        
        # Print key info for debugging (will appear in server logs)
        print(f"\nKey: {self.key.hex()} ({ks}-bit, {self.num_rounds} rounds)")

    def key_expansion(self):
        """
        Expands the cipher key into a key schedule.
        Generates round keys for each round of the encryption process.
        """
        Nk, w = self.key_length//4, [int.from_bytes(self.key[4*i:4*i+4],'big') for i in range(self.key_length//4)]
        for i in range(Nk, 4*(self.num_rounds+1)):
            t = w[i-1]
            if i % Nk == 0:
                # RotWord + SubWord + Rcon
                t = self._sub_word(((t<<8)|(t>>24))&0xFFFFFFFF) ^ (self.RCON[i//Nk-1]<<24)
            elif Nk > 6 and i % Nk == 4:
                # SubWord only for 256-bit keys
                t = self._sub_word(t)
            w.append(w[i-Nk]^t)
        return w
    
    def _sub_word(self, w):
        """Apply S-box to a 4-byte word."""
        return sum(self.S_BOX[(w>>(24-8*i))&0xFF]<<(24-8*i) for i in range(4))

    @staticmethod
    def _gmul(a, b):
        """Galois Field multiplication used in MixColumns."""
        p=0
        for _ in range(8):
            p,a,b = (p^a if b&1 else p),((a<<1)^(0x1b if a&0x80 else 0)),(b>>1)
        return p&0xFF

    def _apply_sbox_shift(self, s, inv):
        """Apply SubBytes and ShiftRows steps (or their inverses)."""
        box = self.INV_S_BOX if inv else self.S_BOX
        for i in range(4):
            # SubBytes: Substitute bytes using S-box
            s[i] = [box[s[i][j]] for j in range(4)]
            # ShiftRows: Cyclically shift rows
            if i>0: s[i] = s[i][-i:]+s[i][:-i] if inv else s[i][i:]+s[i][:i]
        return s
    
    def _mix_col(self, s, inv):
        """Apply MixColumns step (or its inverse)."""
        m = self.MUL[inv]
        for i in range(4):
            c = [s[j][i] for j in range(4)]
            for j in range(4):
                s[j][i] = self._gmul(c[0],m[j][0])^self._gmul(c[1],m[j][1])^self._gmul(c[2],m[j][2])^self._gmul(c[3],m[j][3])
        return s

    def _xor_rk(self, s, r):
        """AddRoundKey: XOR state with round key."""
        rk = [[int.from_bytes(self.round_keys[r*4+j].to_bytes(4,'big')[i:i+1],'big') for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                s[i][j] ^= rk[i][j]
        return s

    def _to_state(self, d):
        """Convert block bytes to state matrix."""
        return [[d[i+4*j] for j in range(4)] for i in range(4)]

    def _from_state(self, s):
        """Convert state matrix to block bytes."""
        return bytes(s[i][j] for j in range(4) for i in range(4))

    def _process_block(self, blk, enc=True):
        """Process a single 128-bit block."""
        s = self._to_state(blk)
        # Initial Round Key Addition
        s = self._xor_rk(s, 0 if enc else self.num_rounds)
        
        # Main Rounds
        for r in (range(1,self.num_rounds) if enc else range(self.num_rounds-1,0,-1)):
            s = self._apply_sbox_shift(s, not enc)
            if enc: s = self._mix_col(s, False)
            s = self._xor_rk(s, r)
            if not enc: s = self._mix_col(s, True)
        
        # Final Round (no MixColumns)
        s = self._apply_sbox_shift(s, not enc)
        s = self._xor_rk(s, self.num_rounds if enc else 0)
        return self._from_state(s)

    def _pad(self, d, u=False):
        """PKCS#7 Padding/Unpadding."""
        if u:
            p=d[-1]
            if p>16 or p==0 or d[-p:]!=bytes([p]*p): raise ValueError("Invalid padding")
            return d[:-p]
        return d+bytes([16-len(d)%16]*(16-len(d)%16))

    def _cbc(self, d, iv, enc=True):
        """CBC (Cipher Block Chaining) Mode."""
        r, p = b'', iv
        for i in range(0,len(d),16):
            b = d[i:i+16]
            if enc:
                # XOR with previous ciphertext (or IV) before encryption
                p = self._process_block(bytes(x^y for x,y in zip(b,p)), True)
                r += p
            else:
                # Decrypt then XOR with previous ciphertext (or IV)
                r += bytes(x^y for x,y in zip(self._process_block(b,False),p))
                p = b
        return r

    def encrypt(self, pt):
        """
        Encrypt plaintext using AES-CBC.
        
        Args:
            pt (str): Plaintext string.
            
        Returns:
            str: Base64 encoded ciphertext.
        """
        self._ensure_key_initialized()
        iv = os.urandom(16) # Generate random Initialization Vector
        # Pad plaintext, encrypt, and prepend IV
        return base64.b64encode(iv+self._cbc(self._pad(pt.encode() if isinstance(pt,str) else pt),iv,True)).decode()

    def decrypt(self, ct):
        """
        Decrypt ciphertext using AES-CBC.
        
        Args:
            ct (str): Base64 encoded ciphertext.
            
        Returns:
            str: Decrypted plaintext.
        """
        self._ensure_key_initialized()
        d = base64.b64decode(ct) if isinstance(ct,str) else ct
        try:
            # Extract IV and decrypt
            return self._pad(self._cbc(d[16:],d[:16],False),True).decode()
        except Exception as e:
            return f"Error: {e}"

    def brute_force(self, ct):
        """
        Calculate feasibility of brute forcing the key.
        """
        return f"Infeasible: AES-{self.key_size} has 2^{self.key_size} = {2**self.key_size:,} possible keys. At 1 billion keys/sec, it would take {2**self.key_size / (10**9 * 60 * 60 * 24 * 365):.2e} years to try all combinations."