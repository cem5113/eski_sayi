# app.py
import streamlit as st
from ancient_numbers_simple import (
    to_roman, to_greek, to_sumerian, to_babylonian, to_egyptian,
    to_devanagari, to_chinese, to_maya, to_aztec
)

st.set_page_config(page_title="Eski Sayı Çevirici", layout="centered")

# ✅ Sonucu büyütmek için CSS
st.markdown("""
<style>
.big-result {
  font-size: 44px !important;
  line-height: 1.25;
  padding: 10px 0;
}
.big-result-egypt {
  font-size: 56px !important;
  line-height: 1.25;
  padding: 10px 0;
}
.big-result-code pre {
  font-size: 34px !important;
  line-height: 1.25;
}
</style>
""", unsafe_allow_html=True)

CIVS = {
    "Sümerler": {
        "warn": "⚠ 60 tabanlı bir sistemdir ancak modern basamaklı yapı tam gelişmemiştir.",
        "symbols": "Sayılar kama işaretlerinin tekrar edilmesiyle yazılır. (𒐕 = 1, 𒌋 = 10, 𒐖 = 60 grubu)",
        "hint": "Örn: 73 → 𒐖 𒌋 𒐕 𒐕 𒐕",
        "min": 0, "max": 10**6,
        "convert": lambda n: to_sumerian(n),
        "format": "text"
    },

    "Babil": {
        "warn": "⚠ 60’lık pozisyonel sistem kullanılır.",
        "symbols": "Sayılar 0–59 arası bloklara ayrılır. Her blok 60’ın kuvvetini temsil eder.",
        "hint": "Örn: 125 → 𒌋𒌋   𒐕𒐕𒐕𒐕𒐕",
        "min": 0,
        "max": 10**6,
        "convert": lambda n: to_babylonian(n),
        "format": "code"   
    },
    
    "Mısırlılar": {
        "warn": "⚠ Toplama gibi: 1000 işaretinden 1 tane, 100 işaretinden 6 tane…",
        "symbols": "1, 10, 100, 1000… için ayrı işaretler vardır ve yan yana tekrar eder.",
        "hint": "Örn: 1655 → 𓆼 + 6×𓍢 + 5×𓎆 + 5×𓏺 (ekranda sembol olarak gösterir)",
        "min": 0, "max": 10**7,
        "convert": lambda n: to_egyptian(n),
        "format": "text"
    },
    "Yunanlar": {
        "warn": "⚠ Harflerle yazılır. (1–9999 arası destekliyoruz.)",
        "symbols": "Harfler sayıyı temsil eder (α, β, γ…).",
        "hint": "Örn: 1655 → ͵αχνεʹ",
        "min": 1, "max": 9999,
        "convert": lambda n: to_greek(n),
        "format": "text"
    },
    "Roma İmparatorluğu": {
        "warn": "⚠ I, V, X, L, C, D, M kullanılır. (1–3999 arası.)",
        "symbols": "I=1, V=5, X=10, L=50, C=100, D=500, M=1000.",
        "hint": "Örn: 1655 → MDCLV",
        "min": 1, "max": 3999,
        "convert": lambda n: to_roman(n),
        "format": "text"
    },
    "Hintliler": {
        "warn": "✅ Günümüzdeki onluk sisteme çok benzer. Sıfır vardır.",
        "symbols": "Rakamların Hint yazımı (Devanagari) gösterilir.",
        "hint": "Örn: 1655 → १६५५",
        "min": 0, "max": 10**12,
        "convert": lambda n: to_devanagari(n),
        "format": "text"
    },
    "Çinliler": {
        "warn": "✅ Çin sayı yazımıyla gösterilir (零 一 二 …).",
        "symbols": "Çin rakamlarıyla yazım.",
        "hint": "Örn: 1655 → 一千六百五十五",
        "min": 0, "max": 10**9,
        "convert": lambda n: to_chinese(n),
        "format": "text"
    },
    "Maya Uygarlığı": {
        "warn": "⚠ 20’lik sistem. Nokta (•) ve çizgi (—) kullanılır. Alt satır birlerdir.",
        "symbols": "• = 1, — = 5. Rakamlar üst üste yazılır (dikey).",
        "hint": "Örn: 1655 → 20’lik basamaklarda dikey görünür.",
        "min": 0, "max": 10**9,
        "convert": lambda n: to_maya(n),
        "format": "code"  # multi-line
    },
    "Aztekler": {
        "warn": "⚠ 20’lik (vigésimal) toplamalı sistem kullanılır.",
        "symbols": "Temel işaretler (temsili gösterim): • = 1, ⚑ = 20 (Pantli), 🪶 = 400 (Tzontli), 🧺 = 8000 (Xiquipilli).",
        "hint": "Örn: 1655 → 🪶🪶🪶🪶  ⚑⚑  •••••••••••••••",
        "min": 0,
        "max": 10**9,
        "convert": lambda n: to_aztec(n),
        "format": "text"
    },
}

# Basit sayfa geçişi: home <-> convert
if "page" not in st.session_state:
    st.session_state.page = "home"
if "civ" not in st.session_state:
    st.session_state.civ = None

def go_home():
    st.session_state.page = "home"
    st.session_state.civ = None

def go_convert(civ_name: str):
    st.session_state.page = "convert"
    st.session_state.civ = civ_name

# ---------------- HOME ----------------
if st.session_state.page == "home":
    st.title("🏺 Eski Sayı Sistemleri Çevirici")
    st.write("Bir uygarlık seç, sayını yaz, çevir! 🙂")

    st.subheader("Uygarlık Seç")
    cols = st.columns(2)
    names = list(CIVS.keys())
    for i, name in enumerate(names):
        with cols[i % 2]:
            if st.button(name, use_container_width=True):
                go_convert(name)

    st.caption('Not: Bu uygulama, Ela EROĞLU’nun Matematik proje ödevi için hazırladığı eğlenceli bir eski sayı çeviricisidir.')

# ---------------- CONVERT ----------------
else:
    civ = st.session_state.civ
    info = CIVS[civ]

    st.title(f"🔎 {civ}")
    st.info(info["warn"])
    st.write("**Bu uygarlıkta nasıl yazılır?**")
    st.write(f"- {info['symbols']}")
    st.write(f"- {info['hint']}")

    st.divider()
    st.subheader("Sayı Gir")

    n = st.number_input(
        "Sayı",
        min_value=int(info["min"]),
        max_value=int(info["max"]),
        value=int(max(0, info["min"])),
        step=1
    )

    if st.button("✨ Çevir", use_container_width=True):
        try:
            result = info["convert"](int(n))
            st.subheader("Sonuç")

            # Maya gibi çok satırlı ise code bloğunu büyüt
            if info["format"] == "code":
                st.markdown("<div class='big-result-code'>", unsafe_allow_html=True)
                st.code(result, language="text")
                st.markdown("</div>", unsafe_allow_html=True)

            # Diğerleri tek satır: büyük font
            else:
                # Mısır daha da büyük
                if civ == "Mısırlılar":
                    st.markdown(f"<div class='big-result-egypt'>{result}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='big-result'>{result}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(str(e))

    st.divider()
    colA, colB = st.columns(2)
    with colA:
        if st.button("⬅ Ana sayfaya dön", use_container_width=True):
            go_home()
    with colB:
        st.caption("İpucu: Başka uygarlık seçmek için ana sayfaya dön.")
