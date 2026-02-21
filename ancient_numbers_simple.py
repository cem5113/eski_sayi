# ancient_numbers_simple.py

# --- Roman ---
_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]

def to_roman(n: int) -> str:
    if not (1 <= n <= 3999):
        raise ValueError("Roma rakamları için 1–3999 arası gir.")
    out = []
    x = n
    for v, s in _ROMAN:
        k, x = divmod(x, v)
        out.append(s * k)
    return "".join(out)

# --- Greek (Ionian) 1..9999 ---
_G_UNITS = {1:"α",2:"β",3:"γ",4:"δ",5:"ε",6:"ϛ",7:"ζ",8:"η",9:"θ"}
_G_TENS  = {10:"ι",20:"κ",30:"λ",40:"μ",50:"ν",60:"ξ",70:"ο",80:"π",90:"ϟ"}
_G_HUND  = {100:"ρ",200:"σ",300:"τ",400:"υ",500:"φ",600:"χ",700:"ψ",800:"ω",900:"ϡ"}
_KERAIA = "ʹ"
_THOUS  = "͵"

def to_greek(n: int) -> str:
    if not (1 <= n <= 9999):
        raise ValueError("Yunan rakamları için 1–9999 arası gir.")
    parts = []
    x = n
    th, x = divmod(x, 1000)
    if th:
        parts.append(_THOUS + _G_UNITS[th])
    h, x = divmod(x, 100)
    if h:
        parts.append(_G_HUND[h*100])
    t, x = divmod(x, 10)
    if t:
        parts.append(_G_TENS[t*10])
    if x:
        parts.append(_G_UNITS[x])
    return "".join(parts) + _KERAIA

# --- Base conversion helpers ---
def _to_base(n: int, base: int) -> list[int]:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    if n == 0:
        return [0]
    d = []
    x = n
    while x:
        x, r = divmod(x, base)
        d.append(r)
    return list(reversed(d))

# --- Sumer/Babylon (base-60) ---
def to_sexagesimal(n: int) -> str:
    # compact like 27;35
    d = _to_base(n, 60)
    return ";".join(str(x) for x in d)

# --- Egyptian (hieroglyphic logic) additive ---
_EGY = [
    (1_000_000, "𓁨"),
    (100_000,   "𓆐"),
    (10_000,    "𓂭"),
    (1_000,     "𓆼"),
    (100,       "𓍢"),
    (10,        "𓎆"),
    (1,         "𓏺"),
]

def to_egyptian(n: int) -> str:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    if n == 0:
        return "0 (Mısır’da sıfır yaygın bir sayı işareti değildi)"
    out = []
    x = n
    for v, sym in _EGY:
        k, x = divmod(x, v)
        if k:
            out.append(sym * k)
    return " ".join(out)

# --- Devanagari digits ---
_DEV = str.maketrans("0123456789", "०१२३४५६७८९")
def to_devanagari(n: int) -> str:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    return str(n).translate(_DEV)

# --- Chinese (simple) ---
_CN = {0:"零",1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九"}
def to_chinese(n: int) -> str:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    if n == 0:
        return _CN[0]

    def chunk(x: int) -> str:
        # 0..9999
        res = []
        q, r = divmod(x, 1000)
        if q: res.append(_CN[q] + "千")
        q, r2 = divmod(r, 100)
        if q: res.append(_CN[q] + "百")
        elif res and r2: res.append("零")
        q, r3 = divmod(r2, 10)
        if q:
            if not res and q == 1:
                res.append("十")
            else:
                res.append(_CN[q] + "十")
        elif res and r3:
            res.append("零")
        if r3:
            res.append(_CN[r3])
        return "".join(res).replace("零零", "零").strip("零")

    w, r = divmod(n, 10_000)
    if w and r:
        return chunk(w) + "万" + chunk(r)
    if w:
        return chunk(w) + "万"
    return chunk(r)

# --- Maya (base-20) with dots/bars stacked ---
def _maya_digit(v: int) -> str:
    if v == 0:
        return "𝟘"
    bars, dots = divmod(v, 5)
    return "—"*bars + "•"*dots

def to_maya(n: int) -> str:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    d = _to_base(n, 20)
    # show highest on top, ones at bottom
    lines = [_maya_digit(v) for v in d]
    return "\n".join(lines)

# --- Aztec (simple additive) ---
_AZ = [
    (8000, "🎒"),
    (400,  "🪶"),
    (20,   "⚑"),
    (1,    "•"),
]

def to_aztec(n: int) -> str:
    if n < 0:
        raise ValueError("Negatif sayı yok 🙂")
    if n == 0:
        return "0 (Azteklerde de sıfır modern anlamda standart değildi)"
    out = []
    x = n
    for v, sym in _AZ:
        k, x = divmod(x, v)
        if k:
            out.append(sym * k)
    return " ".join(out)
