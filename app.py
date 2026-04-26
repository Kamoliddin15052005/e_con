"""
E-Construction — Korrupsiyaga qarshi AI tizimi
Dark Glassmorphism Design | uiverse.io ilhomi
VMQ №200 (20.04.2022) reglamenti asosida
"""

import streamlit as st
import json, os, requests, numpy as np, time
from datetime import datetime
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="E-Construction AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  GLASSMORPHISM CSS  (uiverse.io dark style)
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── GLOBAL ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2e 40%, #0a1628 70%, #0e0a1e 100%);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(10,14,26,0.95) !important;
    border-right: 1px solid rgba(0,212,255,0.15) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Ambient orbs */
[data-testid="stAppViewContainer"]::before {
    content:"";
    position:fixed;top:-200px;left:-200px;
    width:500px;height:500px;
    background:radial-gradient(circle,rgba(0,212,255,0.08) 0%,transparent 70%);
    pointer-events:none;z-index:0;
}
[data-testid="stAppViewContainer"]::after {
    content:"";
    position:fixed;bottom:-200px;right:-200px;
    width:600px;height:600px;
    background:radial-gradient(circle,rgba(124,58,237,0.08) 0%,transparent 70%);
    pointer-events:none;z-index:0;
}

/* ── GLASS CARDS ── */
.glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 8px 0;
    position: relative;
    overflow: hidden;
}
.glass::before {
    content:"";
    position:absolute;top:0;left:0;right:0;
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.4),transparent);
}

.glass-red {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 6px 0;
    position: relative;
}
.glass-red::before {
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(239,68,68,0.6),transparent);
}

.glass-yellow {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 6px 0;
    position: relative;
}
.glass-yellow::before {
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(245,158,11,0.6),transparent);
}

.glass-green {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 6px 0;
    position: relative;
}
.glass-green::before {
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(16,185,129,0.6),transparent);
}

.glass-cyan {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 6px 0;
    position: relative;
}
.glass-cyan::before {
    content:"";position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.5),transparent);
}

/* ── KPI CARDS ── */
.kpi-glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi-glass:hover { transform: translateY(-2px); }
.kpi-val { font-size:42px;font-weight:900;line-height:1.1;letter-spacing:-1px; }
.kpi-lab { font-size:11px;color:#94a3b8;margin-top:6px;text-transform:uppercase;letter-spacing:1px; }

/* ── STEP BADGE ── */
.step {
    display:inline-flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,#00d4ff,#7c3aed);
    color:#fff;border-radius:50%;width:30px;height:30px;
    font-weight:800;font-size:14px;margin-right:10px;
    box-shadow:0 0 12px rgba(0,212,255,0.4);
    vertical-align:middle;
}

/* ── VERDICT BOX ── */
.verdict-high {
    background:linear-gradient(135deg,rgba(239,68,68,0.12),rgba(239,68,68,0.06));
    border:1px solid rgba(239,68,68,0.4);
    border-radius:16px;padding:24px 28px;margin:12px 0;
    box-shadow:0 0 30px rgba(239,68,68,0.15);
}
.verdict-mid {
    background:linear-gradient(135deg,rgba(245,158,11,0.12),rgba(245,158,11,0.06));
    border:1px solid rgba(245,158,11,0.4);
    border-radius:16px;padding:24px 28px;margin:12px 0;
    box-shadow:0 0 30px rgba(245,158,11,0.15);
}
.verdict-low {
    background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.06));
    border:1px solid rgba(16,185,129,0.4);
    border-radius:16px;padding:24px 28px;margin:12px 0;
    box-shadow:0 0 30px rgba(16,185,129,0.15);
}

/* ── METRIC BOX ── */
.metric-glass {
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;padding:16px;text-align:center;
    position:relative;overflow:hidden;
}

/* ── NEON BADGE ── */
.badge-red    { background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);border-radius:20px;padding:3px 12px;font-size:12px;font-weight:600; }
.badge-yellow { background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:20px;padding:3px 12px;font-size:12px;font-weight:600; }
.badge-green  { background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);border-radius:20px;padding:3px 12px;font-size:12px;font-weight:600; }
.badge-cyan   { background:rgba(0,212,255,0.1);color:#00d4ff;border:1px solid rgba(0,212,255,0.25);border-radius:20px;padding:3px 12px;font-size:12px;font-weight:600; }

/* ── TEXT COLORS ── */
h1,h2,h3 { color:#f1f5f9 !important; }
p, li, span, div { color:#cbd5e1; }
label { color:#94a3b8 !important; }
.glow-text { 
    background:linear-gradient(90deg,#00d4ff,#7c3aed);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    font-weight:900;
}

/* ── PROGRESS OVERRIDE ── */
.stProgress>div>div { border-radius:4px !important; }
[data-testid="stProgress"]>div {
    background:rgba(255,255,255,0.06) !important;
    border-radius:4px;
}

/* ── INPUT FIELDS ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
    background:rgba(255,255,255,0.05) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    color:#e2e8f0 !important;
    border-radius:8px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color:rgba(0,212,255,0.4) !important;
    box-shadow:0 0 0 2px rgba(0,212,255,0.1) !important;
}

/* ── BUTTONS ── */
[data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,#00d4ff,#7c3aed) !important;
    border:none !important;
    border-radius:8px !important;
    font-weight:700 !important;
    letter-spacing:0.5px !important;
    box-shadow:0 4px 15px rgba(0,212,255,0.25) !important;
}
[data-testid="baseButton-secondary"] {
    background:rgba(255,255,255,0.06) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    color:#e2e8f0 !important;
    border-radius:8px !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background:rgba(255,255,255,0.03) !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:12px !important;
}
[data-testid="stExpander"] summary { color:#cbd5e1 !important; }

/* ── METRIC ── */
[data-testid="stMetric"] { background:transparent !important; }
[data-testid="stMetricLabel"] { color:#94a3b8 !important; font-size:12px !important; }
[data-testid="stMetricValue"] { color:#f1f5f9 !important; }

/* ── DIVIDER ── */
hr { border-color:rgba(255,255,255,0.08) !important; margin:24px 0 !important; }

/* ── SIDEBAR NAV ── */
[data-testid="stRadio"] label { 
    color:#cbd5e1 !important;
    padding:6px 0 !important;
}
[data-testid="stRadio"] label:hover { color:#00d4ff !important; }

/* ── INFO/WARNING/ERROR ── */
[data-testid="stInfo"]    { background:rgba(0,212,255,0.08) !important; border-color:rgba(0,212,255,0.3) !important; }
[data-testid="stWarning"] { background:rgba(245,158,11,0.08) !important; border-color:rgba(245,158,11,0.3) !important; }
[data-testid="stError"]   { background:rgba(239,68,68,0.08) !important; border-color:rgba(239,68,68,0.3) !important; }
[data-testid="stSuccess"] { background:rgba(16,185,129,0.08) !important; border-color:rgba(16,185,129,0.3) !important; }

/* ── FORM ── */
[data-testid="stForm"] {
    background:rgba(255,255,255,0.02) !important;
    border:1px solid rgba(255,255,255,0.06) !important;
    border-radius:16px !important;
    padding:20px !important;
}

/* ── NUMBER INPUT ── */
[data-testid="stNumberInput"] input {
    background:rgba(255,255,255,0.05) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    color:#e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  DATA STORE
# ══════════════════════════════════════════════════════════════════
DATA_FILE = Path("data/apps.json")
DATA_FILE.parent.mkdir(exist_ok=True)

# VMQ №200 (20.04.2022) asosida my.gov.uz reglamentidagi ariza ma'lumotlari
SAMPLE_DATA = [
    {
        "id": "QB-2024-001",
        "loyiha": "Navruz-Servis 16-qavatli turar-joy majmuasi",
        "tadbirkor": 'MChJ "Navruz-Servis Qurilish"',
        "stir": "302 845 671",
        "manzil": "Toshkent sh., Yunusobod t., Navruz ko'ch., 12",
        "tur": "Ko'p qavatli turar-joy (≥5 qavat)",
        "qavatlar": 16,
        "yer_maydoni": "0.42 ga",
        "bosqich": "qurilish",
        "sana": "2024-03-15",
        "holat": "rad_keyin_tasdiq",
        # ── VMQ 200-son: ariza ma'lumotlari (AI shu matnni tahlil qiladi) ──
        "ariza_malumotlar": {
            "sanitariya_zona_m": 15,
            "suv_oqova_tizimi": False,
            "chiqindi_kamera": False,
            "shamollatish_tizimi": True,
            "yong_in_sprinkler": False,
            "evakuatsiya_zina_soni": 2,
            "evakuatsiya_zina_kenglik_m": 0.9,
            "rei_sinfi": "REI-60",
            "yong_in_signal": False,
            "suv_bosimi_mpa": 0.10,
            "ko_kalamzor_foiz": 12,
            "utilizatsiya_shartnoma": False,
            "seysmik_hisob": False,
            "material_sertifikat": False,
            "mustahkamlik_xulosa": False,
            "loyiha_topshiriqnoma": True,
            "arxitektura_kelishish": True,
            "yer_hujjati": True,
            "litsenziyali_pudrat": True,
            "seysmik_zona_ball": 8,
        },
        "ariza_tavsif": (
            "16-qavatli turar-joy binosi (128 xonadon). Yer maydoni 0.42 ga. "
            "Poydevor: plitali temir-beton. Devor: g'isht + penoplex (10 sm). "
            "Zina: 2 dona, kenglik 0.9 m. Lift: 2 dona. "
            "Yong'in o'chirish tizimi loyihada ko'rsatilmagan. "
            "Sanitariya zona 15 m (norma 25 m). Suv oqova sxemasi yo'q. "
            "Ko'kalamzor 12% (norma 20%). Seysmik hisob-kitob to'liq emas. "
            "Mustahkamlik xulosasi taqdim etilmagan. Material sertifikatlari yo'q."
        ),
        "rad_ariza_tavsif": (
            "16-qavatli turar-joy (128 xonadon). Yer 0.42 ga. "
            "Poydevor: plitali temir-beton. Devor: g'isht + penoplex. "
            "Zina: 2 dona, kenglik 0.9 m. Lift: 2 dona. "
            "Yong'in o'chirish tizimi loyihada ko'rsatilmagan. "
            "Sanitariya zona 15 m. Suv oqova sxemasi yo'q. "
            "Ko'kalamzor 12%. Seysmik hisob-kitob to'liq emas. "
            "Mustahkamlik xulosasi taqdim etilmagan. Sertifikatlar yo'q."
        ),
        "organlar": [
            {
                "nom": "Sanitariya-Epidemiologiya",
                "qaror_1": "rad",
                "sabab_1": "Sanitariya himoya zona 15m — norma 25m. Suv oqova sxemasi yo'q. Chiqindi kamerasi loyihaga kiritilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Yong'in Xavfsizligi",
                "qaror_1": "rad",
                "sabab_1": "Sprinkler tizimi yo'q. Evakuatsiya zinasi 0.9m (norma 1.2m). Signal sensori ko'rsatilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Ekologiya",
                "qaror_1": "tasdiq",
                "sabab_1": "",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Qurilish Bosh Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Mustahkamlik xulosasi yo'q. Seysmik hisob-kitob to'liq emas. Material sertifikatlari taqdim etilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
        ],
        "reviews": [
            {"ism": "Aziz N.", "baho": 2, "fikr": "Liftlar ishlamayapti, zina tor. Sifat yomon", "sana": "2024-09-10"},
            {"ism": "Malika R.", "baho": 1, "fikr": "Yong'in sensori yo'q! Xavfli bino", "sana": "2024-09-15"},
            {"ism": "Jahongir T.", "baho": 2, "fikr": "Derazalar sifatsiz, issiqlik yo'qoladi", "sana": "2024-09-20"},
            {"ism": "Nodira K.", "baho": 1, "fikr": "Kanalizatsiya muammosi bor. Hid keladi", "sana": "2024-10-01"},
            {"ism": "Sardor M.", "baho": 2, "fikr": "Suv bosimi past. Yuqori qavatlar azobda", "sana": "2024-10-05"},
        ],
        "ai_mezon_tahlil": None,
        "ai_verdict": None,
        "_doc_sim": None,
    },
    {
        "id": "QB-2024-002",
        "loyiha": "Chilonzor Biznes-Markaz 9-qavatli ofis binosi",
        "tadbirkor": 'AJ "CityBuild Invest"',
        "stir": "207 613 445",
        "manzil": "Toshkent sh., Chilonzor t., Bunyodkor sh.yo'li, 45",
        "tur": "Tijorat binosi",
        "qavatlar": 9,
        "yer_maydoni": "0.18 ga",
        "bosqich": "foydalanish",
        "sana": "2024-05-20",
        "holat": "tasdiq",
        "ariza_malumotlar": {
            "sanitariya_zona_m": 30,
            "suv_oqova_tizimi": True,
            "chiqindi_kamera": True,
            "shamollatish_tizimi": True,
            "yong_in_sprinkler": True,
            "evakuatsiya_zina_soni": 3,
            "evakuatsiya_zina_kenglik_m": 1.4,
            "rei_sinfi": "REI-90",
            "yong_in_signal": True,
            "suv_bosimi_mpa": 0.18,
            "ko_kalamzor_foiz": 22,
            "utilizatsiya_shartnoma": True,
            "seysmik_hisob": True,
            "material_sertifikat": True,
            "mustahkamlik_xulosa": True,
            "loyiha_topshiriqnoma": True,
            "arxitektura_kelishish": True,
            "yer_hujjati": True,
            "litsenziyali_pudrat": True,
            "seysmik_zona_ball": 8,
        },
        "ariza_tavsif": (
            "9-qavatli ofis binosi. Yer maydoni 0.18 ga. "
            "Poydevor: monolitik temir-beton. Devor: g'isht. "
            "Yong'in: sprinkler, signal, gidrant to'liq. "
            "Evakuatsiya: 3 ta zina, kenglik 1.4 m. REI-90. "
            "Seysmik hisob-kitob 8 ball to'liq. Ko'kalamzor 22%. "
            "Mustahkamlik xulosasi mavjud. Material sertifikatlari taqdim etilgan. "
            "Sanitariya zona 30 m. Suv oqova tizimi loyihada ko'rsatilgan."
        ),
        "rad_ariza_tavsif": "",
        "organlar": [
            {"nom": "Sanitariya-Epidemiologiya", "qaror_1": "tasdiq", "sabab_1": "", "qaror_2": "tasdiq", "sabab_2": ""},
            {"nom": "Yong'in Xavfsizligi", "qaror_1": "tasdiq", "sabab_1": "", "qaror_2": "tasdiq", "sabab_2": ""},
            {"nom": "Ekologiya", "qaror_1": "tasdiq", "sabab_1": "", "qaror_2": "tasdiq", "sabab_2": ""},
            {"nom": "Qurilish Inspeksiyasi", "qaror_1": "tasdiq", "sabab_1": "", "qaror_2": "tasdiq", "sabab_2": ""},
        ],
        "reviews": [
            {"ism": "Bekzod O.", "baho": 5, "fikr": "Ajoyib bino. Barcha talablar bajarilgan", "sana": "2024-11-01"},
            {"ism": "Dilnoza A.", "baho": 4, "fikr": "Yaxshi, faqat parking kichikroq", "sana": "2024-11-10"},
            {"ism": "Farrux H.", "baho": 5, "fikr": "Hammasi zo'r. Sifatli qurilish", "sana": "2024-11-15"},
        ],
        "ai_mezon_tahlil": None,
        "ai_verdict": None,
        "_doc_sim": None,
    },
    {
        "id": "QB-2024-003",
        "loyiha": "Elite-Home 12-qavatli Mirzo-Ulug'bek turar-joy",
        "tadbirkor": 'MChJ "Premium Construction"',
        "stir": "410 227 893",
        "manzil": "Toshkent sh., Mirzo-Ulug'bek t., Qoratosh ko'ch., 8",
        "tur": "Ko'p qavatli turar-joy (≥5 qavat)",
        "qavatlar": 12,
        "yer_maydoni": "0.31 ga",
        "bosqich": "foydalanish",
        "sana": "2024-07-10",
        "holat": "rad_keyin_tasdiq",
        "ariza_malumotlar": {
            "sanitariya_zona_m": 12,
            "suv_oqova_tizimi": False,
            "chiqindi_kamera": False,
            "shamollatish_tizimi": True,
            "yong_in_sprinkler": False,
            "evakuatsiya_zina_soni": 1,
            "evakuatsiya_zina_kenglik_m": 0.8,
            "rei_sinfi": "REI-45",
            "yong_in_signal": False,
            "suv_bosimi_mpa": 0.08,
            "ko_kalamzor_foiz": 8,
            "utilizatsiya_shartnoma": False,
            "seysmik_hisob": False,
            "material_sertifikat": False,
            "mustahkamlik_xulosa": False,
            "loyiha_topshiriqnoma": True,
            "arxitektura_kelishish": True,
            "yer_hujjati": True,
            "litsenziyali_pudrat": True,
            "seysmik_zona_ball": 8,
        },
        "ariza_tavsif": (
            "12-qavatli turar-joy (96 xonadon). Yer 0.31 ga. "
            "Poydevor: plitali. Devor: g'isht. "
            "Zina: 1 dona, kenglik 0.8 m. Lift: 1 dona. "
            "Yong'in o'chirish tizimi loyihada ko'rsatilmagan. "
            "Sanitariya zona 12 m (norma 25 m). Ko'kalamzor 8% (norma 20%). "
            "Seysmik hisob-kitob yo'q. Material sertifikat yo'q. "
            "Mustahkamlik xulosasi taqdim etilmagan. REI-45 (norma REI-90)."
        ),
        "rad_ariza_tavsif": (
            "12-qavatli turar-joy (96 xonadon). Yer 0.31 ga. "
            "Poydevor: plitali. Devor: g'isht. "
            "Zina: 1 dona, kenglik 0.8 m. Lift: 1 dona. "
            "Yong'in o'chirish tizimi loyihada ko'rsatilmagan. "
            "Sanitariya zona 12 m. Ko'kalamzor 8%. "
            "Seysmik hisob-kitob yo'q. Material sertifikat yo'q. "
            "Mustahkamlik xulosasi taqdim etilmagan. REI-45."
        ),
        "organlar": [
            {
                "nom": "Sanitariya-Epidemiologiya",
                "qaror_1": "rad",
                "sabab_1": "Sanitariya zona 12m (norma 25m). Suv oqova sxemasi yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Yong'in Xavfsizligi",
                "qaror_1": "rad",
                "sabab_1": "Sprinkler yo'q. Zina 1 dona 0.8m (norma 1.2m). Signal yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Ekologiya",
                "qaror_1": "rad",
                "sabab_1": "Ko'kalamzor 8% (norma 20%). Utilizatsiya shartnomasi yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
            {
                "nom": "Qurilish Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Mustahkamlik xulosasi yo'q. Seysmik hisob yo'q. Sertifikatlar yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "",
            },
        ],
        "reviews": [
            {"ism": "Ulmas V.", "baho": 1, "fikr": "Dahshat. Xavfli bino. Yong'in signali yo'q", "sana": "2024-10-20"},
            {"ism": "Zulfiya M.", "baho": 1, "fikr": "Bolalarim bilan bu binoda yashamayman!", "sana": "2024-10-25"},
            {"ism": "Sherzod B.", "baho": 2, "fikr": "Sifat past. Derazalar va eshiklar arzon", "sana": "2024-11-01"},
        ],
        "ai_mezon_tahlil": None,
        "ai_verdict": None,
        "_doc_sim": None,
    },
]


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    save_data(SAMPLE_DATA)
    return SAMPLE_DATA


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ══════════════════════════════════════════════════════════════════
#  VMQ 200-SON MEZONLAR (ariza ma'lumotlaridan AI baholaydi)
# ══════════════════════════════════════════════════════════════════
# Bu mezonlar my.gov.uz / VMQ №200 (20.04.2022) reglamentiga asoslanadi
MEZON_RULES = [
    # (kalit, nomi, og'irlik, norma, baholash_funksiya)
    # Sanitariya-Epidemiologiya
    ("sanitariya_zona_m",     "🧪 Sanitariya zona (≥25 m)",        5,
     lambda v: 5 if v >= 25 else (3 if v >= 20 else (1 if v >= 15 else 0))),
    ("suv_oqova_tizimi",      "🧪 Suv oqova tizimi sxemasi",        5,
     lambda v: 5 if v else 0),
    ("chiqindi_kamera",       "🧪 Chiqindi kamerasi loyihada",       4,
     lambda v: 5 if v else 0),
    ("shamollatish_tizimi",   "🧪 Shamollatish tizimi",              4,
     lambda v: 5 if v else 0),
    # Yong'in xavfsizligi
    ("yong_in_sprinkler",     "🔥 Sprinkler/gidrant tizimi",         5,
     lambda v: 5 if v else 0),
    ("evakuatsiya_zina_kenglik_m", "🔥 Evakuatsiya zina ≥1.2m",     5,
     lambda v: 5 if v >= 1.2 else (3 if v >= 1.0 else 0)),
    ("rei_sinfi",             "🔥 Konstruksiya REI sinfi (≥REI-90)", 5,
     lambda v: 5 if "90" in str(v) or "120" in str(v) else (2 if "60" in str(v) else 0)),
    ("yong_in_signal",        "🔥 Avtomatik yong'in signalizatsiyasi", 4,
     lambda v: 5 if v else 0),
    ("suv_bosimi_mpa",        "🔥 Yong'in suv bosimi ≥0.15 MPa",    3,
     lambda v: 5 if v >= 0.15 else (2 if v >= 0.10 else 0)),
    # Ekologiya
    ("ko_kalamzor_foiz",      "🌿 Ko'kalamzorlashtirish ≥20%",      3,
     lambda v: 5 if v >= 20 else (3 if v >= 15 else (1 if v >= 10 else 0))),
    ("utilizatsiya_shartnoma","🌿 Chiqindi utilizatsiya shartnomasi", 3,
     lambda v: 5 if v else 0),
    # Qurilish
    ("loyiha_topshiriqnoma",  "🏗️ Loyiha topshiriqnomasi (AT)",     4,
     lambda v: 5 if v else 0),
    ("arxitektura_kelishish", "🏗️ Arxitektura kelishish xulosa",    4,
     lambda v: 5 if v else 0),
    ("yer_hujjati",           "🏗️ Yer uchastkasi hujjati",           5,
     lambda v: 5 if v else 0),
    ("seysmik_hisob",         "🏗️ Seysmik bardoshlilik hisob-kitob", 5,
     lambda v: 5 if v else 0),
    ("material_sertifikat",   "🏗️ Qurilish materiallari sertifikati", 4,
     lambda v: 5 if v else 0),
    ("mustahkamlik_xulosa",   "🏗️ Mustaqil mustahkamlik xulosasi",  5,
     lambda v: 5 if v else 0),
    ("litsenziyali_pudrat",   "🏗️ Litsenziyali pudrat tashkiloti",   4,
     lambda v: 5 if v else 0),
    # Umumiy
    ("evakuatsiya_zina_soni", "🔥 Evakuatsiya zinalar soni (≥2)",    4,
     lambda v: 5 if v >= 2 else (2 if v == 1 else 0)),
]

MAX_SCORE = sum(r[2] for r in MEZON_RULES)


def ai_score_from_data(malumotlar: dict) -> dict:
    """
    Ariza ma'lumotlaridagi raqamli parametrlardan AI mezon balini hisoblash.
    Bu VMQ 200-son normalariga asoslanadi.
    """
    results = {}
    total_weighted = 0
    max_weighted = 0
    dept_scores = {"🧪 Sanitariya": [0, 0], "🔥 Yong'in": [0, 0], "🌿 Ekologiya": [0, 0], "🏗️ Qurilish": [0, 0]}

    for kalit, nom, ogirlik, baholash in MEZON_RULES:
        val = malumotlar.get(kalit)
        if val is None:
            ball = 0
        else:
            try:
                ball = baholash(val)
            except Exception:
                ball = 0
        weighted = (ball / 5) * ogirlik
        total_weighted += weighted
        max_weighted += ogirlik
        # Bo'lim
        for dept_prefix in dept_scores:
            if nom.startswith(dept_prefix[:3]):
                dept_scores[dept_prefix][0] += weighted
                dept_scores[dept_prefix][1] += ogirlik
                break
        results[kalit] = {"nom": nom, "ball": ball, "ogirlik": ogirlik, "weighted": weighted}

    pct = round(total_weighted / max_weighted * 100, 1) if max_weighted else 0
    dept_pct = {d: round(v[0] / v[1] * 100, 1) if v[1] else 0 for d, v in dept_scores.items()}
    return {"pct": pct, "results": results, "dept_pct": dept_pct}


# ══════════════════════════════════════════════════════════════════
#  HUGGINGFACE
# ══════════════════════════════════════════════════════════════════
HF_TOKEN = ""
try:
    HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))
except Exception:
    HF_TOKEN = os.getenv("HF_TOKEN", "")

EMBED_URL = (
    "https://api-inference.huggingface.co/pipeline/feature-extraction/"
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def hf_headers():
    h = {"Content-Type": "application/json"}
    if HF_TOKEN:
        h["Authorization"] = f"Bearer {HF_TOKEN}"
    return h


@st.cache_data(show_spinner=False, ttl=1800)
def embed(texts: list):
    for _ in range(3):
        try:
            r = requests.post(
                EMBED_URL, headers=hf_headers(),
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=45,
            )
            if r.status_code == 200:
                return np.array(r.json())
            if r.status_code == 503:
                time.sleep(8)
        except Exception:
            time.sleep(4)
    return None


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def jaccard(t1: str, t2: str) -> float:
    w1, w2 = set(t1.lower().split()), set(t2.lower().split())
    return len(w1 & w2) / (len(w1 | w2) + 1e-9)


def doc_sim(t1: str, t2: str) -> dict:
    if not t1.strip() or not t2.strip():
        return {"sim": 0.0, "method": "—", "ok": False}
    vecs = embed([t1, t2])
    if vecs is not None:
        return {"sim": round(cosine(vecs[0], vecs[1]), 4), "method": "Semantic AI (MiniLM-L12)", "ok": True}
    return {"sim": round(jaccard(t1, t2), 4), "method": "Jaccard (fallback)", "ok": False}


# ══════════════════════════════════════════════════════════════════
#  KORRUPSIYA VERDICT
# ══════════════════════════════════════════════════════════════════
def verdict(mezon_pct, doc_sim_pct, avg_rev, holat, rad_bor, reviews):
    flags, score = [], 0
    approved = holat in ("tasdiq", "rad_keyin_tasdiq")

    if rad_bor and doc_sim_pct >= 92 and approved:
        flags.append({
            "icon": "📄", "rang": "red",
            "sarlavha": f"Hujjat o'xshashligi {doc_sim_pct:.0f}% — chegara (92%) oshdi",
            "tavsif": (
                f"Rad etilgan va tasdiqlangan arizalar mazmuni semantik jihatdan {doc_sim_pct:.0f}% bir xil. "
                "Bu shuni anglatadiki, vakolatli organlar rad etgan kamchiliklar bartaraf etilmagan holda "
                "tasdiq berilgan. Pora berish orqali hal qilingan bo'lishi mumkin."
            ),
            "tavsiya": "Prokuratura va O'zbekiston Respublikasi Antikorrupsiya agentligiga xabar bering. Hujjat o'zgarishlarini (diff) talab qiling.",
        })
        score += 40
    elif rad_bor and doc_sim_pct >= 78 and approved:
        flags.append({
            "icon": "📄", "rang": "yellow",
            "sarlavha": f"Hujjat o'xshashligi {doc_sim_pct:.0f}% — shubhali daraja",
            "tavsif": "Minimal o'zgarish aniqlandi. Rad sabablari to'liq bartaraf etilmagan bo'lishi mumkin.",
            "tavsiya": "Qo'shimcha ekspertiza va hujjat audit buyurtma qiling.",
        })
        score += 20

    if mezon_pct < 55 and approved:
        flags.append({
            "icon": "🧮", "rang": "red",
            "sarlavha": f"VMQ 200-son mezon bali {mezon_pct:.0f}% — kritik past, tasdiq berilgan",
            "tavsif": (
                f"Ariza ma'lumotlari VMQ №200 normalari bo'yicha faqat {mezon_pct:.0f}% talabni qondiradi. "
                "Texnik kamchiliklar (yong'in tizimi, seysmik hisob, sanitariya zona) bartaraf etilmagan holda "
                "ruxsatnoma berilgan. Bu normal protsedura doirasida mumkin emas."
            ),
            "tavsiya": "Ruxsatnoma berishda qaysi mezonlar e'tiborga olinmaganini so'rang. Texnik inspeksiya buyurtma qiling.",
        })
        score += 30
    elif mezon_pct < 68 and approved:
        flags.append({
            "icon": "🧮", "rang": "yellow",
            "sarlavha": f"VMQ mezon bali {mezon_pct:.0f}% — me'yordan past (70% talab)",
            "tavsif": "Texnik talablar to'liq bajarilmagan holda tasdiq berilgan.",
            "tavsiya": "Qo'shimcha texnik tekshiruv buyurtma qiling.",
        })
        score += 15

    if reviews and avg_rev <= 2.0 and approved:
        flags.append({
            "icon": "⭐", "rang": "red",
            "sarlavha": f"Aholi bahosi {avg_rev:.1f}/5 — kritik past, rasmiy tasdiqqa zid",
            "tavsif": (
                f"{len(reviews)} ta rezident o'rtacha {avg_rev:.1f} ball berdi — 'qoniqarsiz' daraja. "
                "Rasmiy inspeksiyalar qurilish sifatini 'yaxshi' deb topgan. "
                "Bu inspeksiya to'liq o'tkazilmagan yoki hujjatlar soxtalashtirilib, ruxsat berilgan bo'lishi mumkin."
            ),
            "tavsiya": "Qurilish aktlarini qayta tekshiring. Aholi shikoyatlarini rasman O'zINSPEKTSIYA tizimiga yuboring.",
        })
        score += 28
    elif reviews and avg_rev <= 2.8 and approved:
        flags.append({
            "icon": "⭐", "rang": "yellow",
            "sarlavha": f"Aholi bahosi {avg_rev:.1f}/5 — rasmiy xulosadan past",
            "tavsif": "Aholining qurilish sifatiga bahosi o'rtacha darajadan past.",
            "tavsiya": "Yangi texnik inspeksiya o'tkazing.",
        })
        score += 12

    if score >= 50:
        level, cls = "🔴 YUQORI XAVF", "high"
        umumiy = ("Bir nechta jiddiy korrupsion alomat aniqlandi. Prokuratura va O'zbekiston Respublikasi "
                  "Antikorrupsiya agentligiga darhol xabar berilishi tavsiya etiladi. "
                  "Loyiha hujjatlari va moliyaviy to'lovlar mustaqil audit qilinishi shart. "
                  "Ariza tizimda 🔴 XAVF guruhiga kiritildi.")
    elif score >= 20:
        level, cls = "🟡 O'RTA XAVF", "mid"
        umumiy = ("Ba'zi shubhali ko'rsatkichlar aniqlandi. 30 kun ichida qo'shimcha texnik ekspertiza va "
                  "hujjatlar qayta ko'rib chiqilishi tavsiya etiladi. Ariza kuzatuv ro'yxatiga kiritildi.")
    else:
        level, cls = "🟢 PAST XAVF", "low"
        umumiy = ("Ko'rsatkichlar o'zaro muvofiq. Ariza ma'lumotlari, mezon ballari va aholi baholari mos keladi. "
                  "Oddiy monitoring tartibida davom ettirilsin.")

    return {"level": level, "cls": cls, "flags": flags, "score": score, "umumiy": umumiy}


# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="padding:8px 0 16px 0">', unsafe_allow_html=True)
    st.markdown('<span class="glow-text" style="font-size:22px">🏗️ E-Construction</span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px">Korrupsiyaga qarshi AI</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(0,212,255,0.15);margin:8px 0 16px 0">', unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Bosh sahifa",
        "🔍  AI Tahlil",
        "📋  Arizalar",
        "➕  Yangi ariza",
        "⭐  Jamoatchilik bahosi",
        "📊  Statistika",
    ], label_visibility="collapsed")

    st.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:16px 0">', unsafe_allow_html=True)

    if HF_TOKEN:
        st.markdown('<div class="glass-green" style="padding:10px 14px"><span style="font-size:12px">✅ <b>HF Token</b> ulangan<br><span style="color:#6ee7b7;font-size:11px">Semantic AI faol (MiniLM)</span></span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-yellow" style="padding:10px 14px"><span style="font-size:12px">⚠️ <b>HF Token</b> yo\'q<br><span style="color:#fcd34d;font-size:11px">Jaccard fallback rejim</span></span></div>', unsafe_allow_html=True)
        with st.expander("🔑 Token ulash"):
            st.markdown("""
```toml
# .streamlit/secrets.toml
HF_TOKEN = "hf_xxxxx"
```
[huggingface.co](https://huggingface.co) → Settings → Access Tokens → New (Read)
            """)


# ══════════════════════════════════════════════════════════════════
#  BOSH SAHIFA
# ══════════════════════════════════════════════════════════════════
if page == "🏠  Bosh sahifa":
    st.markdown('<h1 class="glow-text" style="font-size:36px;margin-bottom:4px">E-Construction AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:15px;margin-bottom:24px">Qurilish ruxsatnomalari jarayonidagi korrupsion alomatlarni aniqlash tizimi</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-cyan">
    <b style="color:#00d4ff">🤖 AI qanday ishlaydi:</b><br><br>
    <span class="step">1</span><span style="color:#e2e8f0">Ariza ma'lumotlari VMQ №200 reglament mezonlari bo'yicha AI tahlil qiladi</span><br><br>
    <span class="step">2</span><span style="color:#e2e8f0">Rad etilgan va tasdiqlangan arizalar semantik jihatdan taqqoslanadi</span><br><br>
    <span class="step">3</span><span style="color:#e2e8f0">Jamoatchilik yulduzli baholari rasmiy xulosaga solishtiriladi</span><br><br>
    <span class="step">4</span><span style="color:#e2e8f0">AI barcha ko'rsatkichlarni birlashtiradi va korrupsiya xavfini bildiradi</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    apps = load_data()

    all_v = []
    for a in apps:
        m = ai_score_from_data(a.get("ariza_malumotlar", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        dsim = 0
        if rad_bor:
            t1, t2 = a.get("rad_ariza_tavsif", ""), a.get("ariza_tavsif", "")
            if t1 and t2:
                w1, w2 = set(t1.lower().split()), set(t2.lower().split())
                dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(m["pct"], dsim, avg, a["holat"], rad_bor, revs)
        all_v.append(v["score"])

    red_cnt = sum(1 for s in all_v if s >= 50)
    yel_cnt = sum(1 for s in all_v if 20 <= s < 50)
    rad_cnt = len([a for a in apps if a["holat"] == "rad_keyin_tasdiq"])

    col1, col2, col3, col4 = st.columns(4)
    kpi_data = [
        (col1, str(len(apps)), "JAMI ARIZALAR", "#00d4ff"),
        (col2, str(red_cnt), "🔴 YUQORI XAVF", "#ef4444"),
        (col3, str(yel_cnt), "🟡 O'RTA XAVF", "#f59e0b"),
        (col4, str(rad_cnt), "⚠️ RAD→TASDIQ", "#a855f7"),
    ]
    for col, val, lab, clr in kpi_data:
        col.markdown(
            f'<div class="kpi-glass">'
            f'<div class="kpi-val" style="color:{clr};text-shadow:0 0 20px {clr}40">{val}</div>'
            f'<div class="kpi-lab">{lab}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<h3 style="color:#f1f5f9">⚡ Arizalar tezkor ko\'rinishi</h3>', unsafe_allow_html=True)

    for i, a in enumerate(apps):
        m = ai_score_from_data(a.get("ariza_malumotlar", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        t1 = a.get("rad_ariza_tavsif", "")
        t2 = a.get("ariza_tavsif", "")
        dsim = 0
        if rad_bor and t1 and t2:
            w1, w2 = set(t1.lower().split()), set(t2.lower().split())
            dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(m["pct"], dsim, avg, a["holat"], rad_bor, revs)

        score_icon = "🔴" if v["score"] >= 50 else ("🟡" if v["score"] >= 20 else "🟢")
        badge_cls = "badge-red" if v["score"] >= 50 else ("badge-yellow" if v["score"] >= 20 else "badge-green")
        hol_map = {"tasdiq": "✅ Tasdiq", "rad_keyin_tasdiq": "⚠️ Rad→Tasdiq", "rad": "🚫 Rad"}

        with st.expander(f"{score_icon} **{a['id']}** — {a['loyiha']}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("VMQ Mezon", f"{m['pct']:.0f}%")
            c2.metric("Hujjat sim.", f"{dsim:.0f}%" if rad_bor else "—")
            c3.metric("Aholi bahosi", f"{avg:.1f}⭐" if revs else "—")
            c4.metric("Xavf bali", str(v["score"]))
            c5.metric("Holat", hol_map.get(a["holat"], "?"))

            if v["flags"]:
                for fl in v["flags"]:
                    cls_map = {"red": "glass-red", "yellow": "glass-yellow"}
                    st.markdown(
                        f'<div class="{cls_map.get(fl["rang"], "glass-cyan")}">'
                        f'<b>{fl["icon"]} {fl["sarlavha"]}</b></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown('<div class="glass-green">✅ Aniqlanadigan korrupsion alomat yo\'q</div>', unsafe_allow_html=True)

            if st.button(f"🔍 To'liq AI tahlil", key=f"h{i}", type="primary"):
                st.session_state["sel_id"] = a["id"]
                st.rerun()


# ══════════════════════════════════════════════════════════════════
#  AI TAHLIL
# ══════════════════════════════════════════════════════════════════
elif page == "🔍  AI Tahlil":
    st.markdown('<h1 class="glow-text">🔍 AI Korrupsiya Tahlili</h1>', unsafe_allow_html=True)
    apps = load_data()

    default_idx = 0
    if "sel_id" in st.session_state:
        ids = [a["id"] for a in apps]
        if st.session_state["sel_id"] in ids:
            default_idx = ids.index(st.session_state["sel_id"])

    sel_id = st.selectbox(
        "Ariza:",
        [a["id"] for a in apps],
        index=default_idx,
        format_func=lambda x: f"{x} — {next(a['loyiha'] for a in apps if a['id']==x)}",
    )
    app = next(a for a in apps if a["id"] == sel_id)

    hol_map = {"tasdiq": "✅ Tasdiqlandi", "rad_keyin_tasdiq": "⚠️ Rad → Keyin tasdiq", "rad": "🚫 Rad etildi"}
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="glass"><b style="color:#00d4ff">{app["loyiha"]}</b><br><span style="font-size:13px;color:#94a3b8">📍 {app["manzil"]}</span></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="glass"><span style="color:#94a3b8;font-size:12px">TUR</span><br><b style="color:#e2e8f0">{app["tur"]}</b><br><span style="color:#94a3b8;font-size:12px">STIR: {app.get("stir","—")}</span></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="glass"><span style="color:#94a3b8;font-size:12px">HOLAT</span><br><b style="color:#e2e8f0">{hol_map.get(app["holat"],"?")}</b><br><span style="color:#94a3b8;font-size:12px">{app["sana"]}</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ═══ QADAM 1: AI MEZON TAHLILI (ariza ma'lumotlaridan) ═══
    st.markdown('<div><span class="step">1</span><b style="color:#f1f5f9;font-size:17px">VMQ №200 Mezon tahlili — Ariza ma\'lumotlaridan AI baholaydi</b></div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:13px;margin:4px 0 12px 40px">VМQ №200 (20.04.2022) reglamentiga asoslanadi — my.gov.uz rasmiy talablari</p>', unsafe_allow_html=True)

    mezon_data = ai_score_from_data(app.get("ariza_malumotlar", {}))
    mezon_pct = mezon_data["pct"]

    clr_bar = "#10b981" if mezon_pct >= 70 else ("#f59e0b" if mezon_pct >= 55 else "#ef4444")
    cbar, cval = st.columns([4, 1])
    cbar.progress(mezon_pct / 100, text=f"Ariza VMQ mezon muvofiqlik: **{mezon_pct:.0f}%** (talab: ≥70%)")
    cval.markdown(f'<div style="text-align:center;color:{clr_bar};font-weight:800;font-size:22px;padding-top:4px">{mezon_pct:.0f}%</div>', unsafe_allow_html=True)

    # Bo'lim breakdown
    dcols = st.columns(4)
    for i, (dept, dp) in enumerate(mezon_data["dept_pct"].items()):
        clr = "#ef4444" if dp < 60 else ("#f59e0b" if dp < 75 else "#10b981")
        dcols[i].markdown(
            f'<div class="metric-glass" style="border-top:3px solid {clr}">'
            f'<div style="font-size:12px;color:#94a3b8;margin-bottom:4px">{dept}</div>'
            f'<div style="font-size:28px;font-weight:800;color:{clr}">{dp:.0f}%</div>'
            f'</div>', unsafe_allow_html=True,
        )

    with st.expander("📋 Barcha mezon ballari (VMQ №200 normalari)"):
        st.markdown('<div class="glass-cyan" style="font-size:12px;padding:10px 14px;margin-bottom:12px"><b>📌 Reglament:</b> O\'zbekiston Respublikasi Vazirlar Mahkamasining 2022-yil 20-apreldagi №200-sonli qarori — Qurilish sohasiga oid yagona ma\'muriy reglamentlar (my.gov.uz)</div>', unsafe_allow_html=True)
        for kalit, nom, ogirlik, _ in MEZON_RULES:
            r = mezon_data["results"].get(kalit, {})
            ball = r.get("ball", 0)
            clr = "#ef4444" if ball <= 1 else ("#f59e0b" if ball <= 3 else "#10b981")
            dots = "●" * ball + "○" * (5 - ball)
            val = app.get("ariza_malumotlar", {}).get(kalit)
            val_str = str(val) if val is not None else "—"
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">'
                f'<span style="flex:1;font-size:13px;color:#cbd5e1">{nom}</span>'
                f'<span style="font-size:11px;color:#64748b;min-width:60px">{val_str}</span>'
                f'<span style="color:{clr};font-size:13px;letter-spacing:2px">{dots}</span>'
                f'<span style="color:{clr};font-weight:700;width:30px;text-align:right">{ball}/5</span>'
                f'<span style="color:#475569;font-size:11px">×{ogirlik}</span>'
                f'</div>', unsafe_allow_html=True,
            )

    st.markdown("---")

    # ═══ QADAM 2: ORGANLAR VA HUJJAT TAQQOSLASH ═══
    rad_bor = app["holat"] == "rad_keyin_tasdiq"
    doc_sim_pct = (app.get("_doc_sim") or 0) * 100

    st.markdown('<div><span class="step">2</span><b style="color:#f1f5f9;font-size:17px">Vakolatli organlar qarorlari</b></div>', unsafe_allow_html=True)
    st.markdown("")

    for org in app.get("organlar", []):
        q1 = org["qaror_1"]
        q2 = org["qaror_2"]
        icon1 = "🔴 Rad" if q1 == "rad" else "✅ Tasdiq"
        icon2 = "🔴 Rad" if q2 == "rad" else "✅ Tasdiq"
        with st.expander(f"**{org['nom']}** │ {icon1} → {icon2}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**1-qaror: {icon1}**")
                if org.get("sabab_1"):
                    st.markdown(f'<div class="glass-red"><span style="font-size:13px">{org["sabab_1"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="glass-green"><span style="font-size:13px">Sabab yo\'q — bevosita tasdiq</span></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f"**2-qaror: {icon2}**")
                if org.get("sabab_2"):
                    st.markdown(f'<div class="glass-green"><span style="font-size:13px">{org["sabab_2"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="glass-green"><span style="font-size:13px">Sabab yo\'q — tasdiq</span></div>', unsafe_allow_html=True)

    if rad_bor:
        st.markdown("")
        st.markdown(f'<div class="glass-yellow"><b>📄 Semantic AI hujjat taqqoslash:</b> Rad va tasdiq arizalari mazmuni qanchalik bir xil?</div>', unsafe_allow_html=True)
        if st.button("🤖 MiniLM semantic taqqoslash", type="primary", key="doc_cmp"):
            t1 = app.get("rad_ariza_tavsif", "")
            t2 = app.get("ariza_tavsif", "")
            with st.spinner("HuggingFace MiniLM-L12 tahlil qilmoqda..."):
                res = doc_sim(t1, t2)
            sim = res["sim"] * 100
            doc_sim_pct = sim
            thresh = 92
            if sim >= thresh:
                st.markdown(f'<div class="glass-red"><b>🚨 O\'xshashlik {sim:.1f}%</b> — chegara ({thresh}%) oshdi! Hujjatlar deyarli bir xil.<br><small style="color:#94a3b8">Usul: {res["method"]}</small></div>', unsafe_allow_html=True)
            elif sim >= 78:
                st.markdown(f'<div class="glass-yellow"><b>⚠️ O\'xshashlik {sim:.1f}%</b> — shubhali daraja.<br><small style="color:#94a3b8">Usul: {res["method"]}</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="glass-green"><b>✅ O\'xshashlik {sim:.1f}%</b> — hujjatlar farqlanadi.<br><small style="color:#94a3b8">Usul: {res["method"]}</small></div>', unsafe_allow_html=True)

            apps2 = load_data()
            for a2 in apps2:
                if a2["id"] == sel_id:
                    a2["_doc_sim"] = res["sim"]
            save_data(apps2)
            app["_doc_sim"] = res["sim"]

        if app.get("_doc_sim"):
            doc_sim_pct = app["_doc_sim"] * 100

    st.markdown("---")

    # ═══ QADAM 3: JAMOATCHILIK BAHOSI NATIJASI ═══
    st.markdown('<div><span class="step">3</span><b style="color:#f1f5f9;font-size:17px">Jamoatchilik bahosi natijalari</b></div>', unsafe_allow_html=True)
    st.markdown("")

    reviews = app.get("reviews", [])
    avg_rev = np.mean([r["baho"] for r in reviews]) if reviews else 0

    if reviews:
        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            clr = "#ef4444" if avg_rev <= 2.5 else ("#f59e0b" if avg_rev <= 3.5 else "#10b981")
            st.markdown(
                f'<div class="metric-glass" style="border-top:4px solid {clr};padding:20px">'
                f'<div style="font-size:13px;color:#94a3b8;margin-bottom:8px">O\'RTACHA BAHO</div>'
                f'<div style="font-size:44px;font-weight:900;color:{clr};text-shadow:0 0 20px {clr}40">{avg_rev:.1f}</div>'
                f'<div style="font-size:18px;margin:4px 0">{"⭐" * round(avg_rev)}{"☆" * (5-round(avg_rev))}</div>'
                f'<div style="font-size:12px;color:#64748b">{len(reviews)} ta baho</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            from collections import Counter
            dist = Counter(r["baho"] for r in reviews)
            st.markdown("<br>", unsafe_allow_html=True)
            for i in range(5, 0, -1):
                cnt = dist.get(i, 0)
                bar_pct = cnt / len(reviews) if reviews else 0
                clr_b = "#ef4444" if i <= 2 else ("#f59e0b" if i == 3 else "#10b981")
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0">'
                    f'<span style="font-size:11px;width:24px;color:#94a3b8">{"⭐"*i}</span>'
                    f'<div style="flex:1;height:8px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden">'
                    f'<div style="width:{bar_pct*100:.0f}%;height:100%;background:{clr_b};border-radius:4px"></div></div>'
                    f'<span style="font-size:12px;color:#64748b;width:20px">{cnt}</span></div>',
                    unsafe_allow_html=True,
                )
        with c3:
            st.markdown("**Oxirgi sharhlar:**")
            for r in reviews[-4:]:
                clr_r = "#ef4444" if r["baho"] <= 2 else ("#f59e0b" if r["baho"] == 3 else "#10b981")
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.03);border-left:3px solid {clr_r};padding:8px 12px;border-radius:0 8px 8px 0;margin:4px 0">'
                    f'<div style="font-size:12px;font-weight:600;color:#e2e8f0">{r["ism"]} {"⭐"*r["baho"]}</div>'
                    f'<div style="font-size:12px;color:#94a3b8;margin-top:3px">{r["fikr"]}</div>'
                    f'<div style="font-size:11px;color:#475569;margin-top:3px">{r["sana"]}</div></div>',
                    unsafe_allow_html=True,
                )
    else:
        st.markdown('<div class="glass">⭐ Hali jamoatchilik bahosi mavjud emas. "⭐ Jamoatchilik bahosi" bo\'limida baho qo\'shing.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ═══ QADAM 4: AI XULOSA ═══
    st.markdown('<div><span class="step">4</span><b style="color:#f1f5f9;font-size:17px">AI Korrupsiya xulosasi</b></div>', unsafe_allow_html=True)
    st.markdown("")

    prev = app.get("ai_verdict")
    if prev:
        st.markdown(f'<div class="glass-cyan" style="font-size:13px">⏱️ Oxirgi tahlil: <b>{prev["sana"]}</b> | Daraja: <b>{prev["daraja"]}</b> | Ball: {prev["ball"]}</div>', unsafe_allow_html=True)

    if st.button("🤖 AI barcha ko'rsatkichlarni tahlil qilsin", type="primary", use_container_width=True):
        with st.spinner("AI tahlil qilmoqda..."):
            v = verdict(mezon_pct, doc_sim_pct, avg_rev, app["holat"], rad_bor, reviews)

        # Verdict box
        verdict_cls = {"high": "verdict-high", "mid": "verdict-mid", "low": "verdict-low"}[v["cls"]]
        verdict_clr = {"high": "#ef4444", "mid": "#f59e0b", "low": "#10b981"}[v["cls"]]
        st.markdown(
            f'<div class="{verdict_cls}">'
            f'<div style="font-size:22px;font-weight:900;color:{verdict_clr};margin-bottom:10px">{v["level"]}</div>'
            f'<div style="color:#cbd5e1;line-height:1.7">{v["umumiy"]}</div>'
            f'<div style="margin-top:12px"><span class="badge-{"red" if v["score"]>=50 else ("yellow" if v["score"]>=20 else "green")}">Xavf bali: {v["score"]}/100</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # 3 ko'rsatkich
        st.markdown('<b style="color:#f1f5f9">📊 Uch ko\'rsatkich taqqosi:</b>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1:
            c = "#ef4444" if mezon_pct < 55 else ("#f59e0b" if mezon_pct < 70 else "#10b981")
            lbl = "❌ Kritik past" if mezon_pct < 55 else ("⚠️ Chegaraviy" if mezon_pct < 70 else "✅ Normal")
            st.markdown(
                f'<div class="metric-glass" style="border-top:4px solid {c}">'
                f'<div style="font-size:12px;color:#94a3b8;margin-bottom:8px">🧮 VMQ MEZON</div>'
                f'<div style="font-size:36px;font-weight:800;color:{c}">{mezon_pct:.0f}%</div>'
                f'<div style="font-size:12px;color:{c};margin-top:6px">{lbl}</div></div>',
                unsafe_allow_html=True,
            )
        with t2:
            if rad_bor and doc_sim_pct > 0:
                c = "#ef4444" if doc_sim_pct >= 92 else ("#f59e0b" if doc_sim_pct >= 78 else "#10b981")
                lbl = "❌ Xavfli (≥92%)" if doc_sim_pct >= 92 else ("⚠️ Shubhali" if doc_sim_pct >= 78 else "✅ Normal")
                val = f"{doc_sim_pct:.0f}%"
            else:
                c = "#475569"; lbl = "Tekshirilmagan"; val = "—"
            st.markdown(
                f'<div class="metric-glass" style="border-top:4px solid {c}">'
                f'<div style="font-size:12px;color:#94a3b8;margin-bottom:8px">📄 HUJJAT O\'XSHASHLIGI</div>'
                f'<div style="font-size:36px;font-weight:800;color:{c}">{val}</div>'
                f'<div style="font-size:12px;color:{c};margin-top:6px">{lbl}</div></div>',
                unsafe_allow_html=True,
            )
        with t3:
            if reviews:
                c = "#ef4444" if avg_rev <= 2.5 else ("#f59e0b" if avg_rev <= 3.5 else "#10b981")
                lbl = "❌ Qoniqarsiz" if avg_rev <= 2.5 else ("⚠️ O'rtacha" if avg_rev <= 3.5 else "✅ Yaxshi")
                val = f"{avg_rev:.1f}⭐"
            else:
                c = "#475569"; lbl = "Baho yo'q"; val = "—"
            st.markdown(
                f'<div class="metric-glass" style="border-top:4px solid {c}">'
                f'<div style="font-size:12px;color:#94a3b8;margin-bottom:8px">⭐ AHOLI BAHOSI</div>'
                f'<div style="font-size:36px;font-weight:800;color:{c}">{val}</div>'
                f'<div style="font-size:12px;color:{c};margin-top:6px">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

        # Xavf omillari
        if v["flags"]:
            st.markdown('<br><b style="color:#f1f5f9">⚠️ Aniqlangan korrupsion alomatlar:</b>', unsafe_allow_html=True)
            for idx, fl in enumerate(v["flags"], 1):
                cls_map = {"red": "glass-red", "yellow": "glass-yellow"}
                with st.expander(f"{fl['icon']} **{idx}. {fl['sarlavha']}**", expanded=True):
                    st.markdown(f'<div class="{cls_map.get(fl["rang"], "glass-cyan")}"><b>Tavsif:</b><br><span style="font-size:13px">{fl["tavsif"]}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="glass-cyan"><b>💡 Tavsiya:</b><br><span style="font-size:13px">{fl["tavsiya"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-green">✅ Aniqlanadigan korrupsion alomat topilmadi</div>', unsafe_allow_html=True)

        # Saqlash
        apps2 = load_data()
        for a2 in apps2:
            if a2["id"] == sel_id:
                a2["ai_verdict"] = {"sana": datetime.now().strftime("%Y-%m-%d %H:%M"), "daraja": v["level"], "ball": v["score"]}
        save_data(apps2)

    elif not prev:
        st.markdown('<div class="glass-cyan" style="text-align:center;padding:30px">🤖 Yuqoridagi tugmani bosib AI tahlil qildiring</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  ARIZALAR RO'YXATI
# ══════════════════════════════════════════════════════════════════
elif page == "📋  Arizalar":
    st.markdown('<h1 class="glow-text">📋 Arizalar ro\'yxati</h1>', unsafe_allow_html=True)
    apps = load_data()

    filter_h = st.selectbox("Filter:", ["Hammasi", "rad_keyin_tasdiq", "tasdiq", "rad"])
    filtered = apps if filter_h == "Hammasi" else [a for a in apps if a["holat"] == filter_h]

    for i, a in enumerate(filtered):
        m = ai_score_from_data(a.get("ariza_malumotlar", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        t1, t2 = a.get("rad_ariza_tavsif", ""), a.get("ariza_tavsif", "")
        dsim = 0
        if rad_bor and t1 and t2:
            w1, w2 = set(t1.lower().split()), set(t2.lower().split())
            dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(m["pct"], dsim, avg, a["holat"], rad_bor, revs)
        icon = "🔴" if v["score"] >= 50 else ("🟡" if v["score"] >= 20 else "🟢")
        hol_icons = {"tasdiq": "✅", "rad_keyin_tasdiq": "⚠️", "rad": "🚫"}

        with st.expander(f"{icon} **{a['id']}** | {a['loyiha']} {hol_icons.get(a['holat'],'?')}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("VMQ Mezon", f"{m['pct']:.0f}%")
            c2.metric("Hujjat", f"{dsim:.0f}%" if rad_bor else "—")
            c3.metric("Baho", f"{avg:.1f}⭐" if revs else "—")
            c4.metric("Xavf bali", v["score"])
            c5.metric("STIR", a.get("stir", "—"))
            if st.button("🔍 AI tahlil", key=f"lst{i}", type="primary"):
                st.session_state["sel_id"] = a["id"]
                st.rerun()


# ══════════════════════════════════════════════════════════════════
#  YANGI ARIZA — VMQ 200-son reglamenti bo'yicha
# ══════════════════════════════════════════════════════════════════
elif page == "➕  Yangi ariza":
    st.markdown('<h1 class="glow-text">➕ Yangi ariza</h1>', unsafe_allow_html=True)
    st.markdown('<div class="glass-cyan" style="font-size:13px"><b>📌 Reglament:</b> VMQ №200 (20.04.2022) — Qurilish sohasiga oid yagona ma\'muriy reglamentlar asosida my.gov.uz orqali topshirilgan ariza ma\'lumotlari kiritiladi</div>', unsafe_allow_html=True)
    st.markdown("")

    with st.form("new_app_form"):
        st.markdown('<b style="color:#00d4ff">📋 Asosiy ma\'lumotlar</b>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            nid       = st.text_input("Ariza raqami (my.gov.uz)", placeholder="QB-2024-004")
            loyiha    = st.text_input("Loyiha nomi")
            tadbirkor = st.text_input("Buyurtmachi tashkilot")
            stir      = st.text_input("STIR raqami", placeholder="302 845 671")
        with c2:
            manzil   = st.text_input("Obyekt manzili")
            tur      = st.selectbox("Loyiha turi", [
                "Ko'p qavatli turar-joy (≥5 qavat)",
                "Ko'p qavatli turar-joy (<5 qavat)",
                "Tijorat binosi",
                "Ishlab chiqarish obyekti",
                "Ijtimoiy obyekt",
            ])
            qavatlar   = st.number_input("Qavatlar soni", 1, 50, 10)
            yer_maydoni = st.text_input("Yer uchastkasi maydoni", placeholder="0.35 ga")
            bosqich    = st.selectbox("Ruxsatnoma bosqichi", ["qurilish", "foydalanish"])
            holat      = st.selectbox("Ariza holati", ["rad_keyin_tasdiq", "tasdiq", "rad"])

        st.markdown("---")
        st.markdown('<b style="color:#00d4ff">📊 VMQ №200 Texnik parametrlar (ariza ma\'lumotlari)</b>', unsafe_allow_html=True)
        st.markdown('<span style="font-size:12px;color:#64748b">Shu ma\'lumotlar asosida AI 20 mezon bo\'yicha baholaydi</span>', unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown("**🧪 Sanitariya-Epidemiologiya**")
            san_zona  = st.number_input("Sanitariya himoya zona (m)", 0, 100, 15)
            suv_oqova = st.checkbox("Suv oqova tizimi sxemasi loyihada bor")
            chiqindi  = st.checkbox("Chiqindi saqlash kamerasi bor")
            shamollat = st.checkbox("Shamollatish tizimi loyihada bor")
            st.markdown("**🌿 Ekologiya**")
            ko_kalam  = st.number_input("Ko'kalamzorlashtirish (%)", 0, 100, 10)
            utilizat  = st.checkbox("Chiqindi utilizatsiya shartnomasi bor")
        with m2:
            st.markdown("**🔥 Yong'in Xavfsizligi**")
            sprinkler  = st.checkbox("Sprinkler/gidrant tizimi loyihada bor")
            evak_soni  = st.number_input("Evakuatsiya zinalar soni", 0, 10, 1)
            evak_keng  = st.number_input("Evakuatsiya zina kengligi (m)", 0.0, 5.0, 0.9, 0.1)
            rei_sinfi  = st.selectbox("Konstruksiya REI sinfi", ["REI-45","REI-60","REI-90","REI-120"])
            yong_signal = st.checkbox("Avtomatik yong'in signalizatsiyasi bor")
            suv_bosimi = st.number_input("Yong'in suv bosimi (MPa)", 0.0, 1.0, 0.10, 0.01)

        st.markdown("**🏗️ Qurilish va umumiy hujjatlar**")
        q1, q2, q3, q4 = st.columns(4)
        seysmik  = q1.checkbox("Seysmik bardoshlilik hisob-kitob bor")
        material = q2.checkbox("Material sertifikatlari bor")
        mustah   = q3.checkbox("Mustahkamlik xulosasi bor")
        litsenz  = q4.checkbox("Litsenziyali pudrat tashkiloti")
        q5, q6, q7, _ = st.columns(4)
        loyiha_top  = q5.checkbox("Loyiha topshiriqnomasi (AT) bor", value=True)
        arx_kel     = q6.checkbox("Arxitektura kelishish xulosa bor", value=True)
        yer_hujjat  = q7.checkbox("Yer uchastkasi hujjati bor", value=True)
        seysmik_ball = st.number_input("Seysmik zona (ball)", 0, 10, 8)

        st.markdown("---")
        st.markdown('<b style="color:#00d4ff">📄 Ariza tavsifi (loyiha hujjat matni)</b>', unsafe_allow_html=True)
        ariza_tavsif = st.text_area("Tasdiqlangan/Joriy ariza hujjat tavsifi:", height=100,
                                     placeholder="Bino parametrlari, tizimlar, materiallar...")
        if holat == "rad_keyin_tasdiq":
            rad_tavsif = st.text_area("Rad etilgan ariza hujjat tavsifi:", height=100,
                                       placeholder="Birinchi marta topshirilgan hujjat tavsifi...")
        else:
            rad_tavsif = ""

        st.markdown("---")
        st.markdown('<b style="color:#00d4ff">🏛️ Vakolatli organlar qarorlari</b>', unsafe_allow_html=True)
        org_data = []
        for org_nom in ["Sanitariya-Epidemiologiya", "Yong'in Xavfsizligi", "Ekologiya", "Qurilish Inspeksiyasi"]:
            with st.expander(org_nom):
                oc1, oc2 = st.columns(2)
                with oc1:
                    q1_sel = st.selectbox("1-qaror:", ["tasdiq", "rad"], key=f"q1_{org_nom}")
                    # Faqat rad bo'lganda sabab maydoni ko'rinadi
                    if q1_sel == "rad":
                        s1 = st.text_area("Rad sababi (1):", key=f"s1_{org_nom}", height=70)
                    else:
                        s1 = ""
                with oc2:
                    q2_sel = st.selectbox("2-qaror:", ["tasdiq", "rad"], key=f"q2_{org_nom}")
                    if q2_sel == "rad":
                        s2 = st.text_area("Rad sababi (2):", key=f"s2_{org_nom}", height=70)
                    else:
                        s2 = ""
                org_data.append({"nom": org_nom, "qaror_1": q1_sel, "sabab_1": s1, "qaror_2": q2_sel, "sabab_2": s2})

        if st.form_submit_button("💾 Saqlash va AI tahlilga yuborish", type="primary", use_container_width=True):
            if not nid or not loyiha:
                st.error("Ariza raqami va loyiha nomini kiriting!")
            else:
                apps2 = load_data()
                if any(a["id"] == nid for a in apps2):
                    st.error(f"ID {nid} allaqachon mavjud!")
                else:
                    malumotlar = {
                        "sanitariya_zona_m": san_zona,
                        "suv_oqova_tizimi": suv_oqova,
                        "chiqindi_kamera": chiqindi,
                        "shamollatish_tizimi": shamollat,
                        "yong_in_sprinkler": sprinkler,
                        "evakuatsiya_zina_soni": int(evak_soni),
                        "evakuatsiya_zina_kenglik_m": evak_keng,
                        "rei_sinfi": rei_sinfi,
                        "yong_in_signal": yong_signal,
                        "suv_bosimi_mpa": suv_bosimi,
                        "ko_kalamzor_foiz": int(ko_kalam),
                        "utilizatsiya_shartnoma": utilizat,
                        "seysmik_hisob": seysmik,
                        "material_sertifikat": material,
                        "mustahkamlik_xulosa": mustah,
                        "loyiha_topshiriqnoma": loyiha_top,
                        "arxitektura_kelishish": arx_kel,
                        "yer_hujjati": yer_hujjat,
                        "litsenziyali_pudrat": litsenz,
                        "seysmik_zona_ball": int(seysmik_ball),
                    }
                    apps2.append({
                        "id": nid, "loyiha": loyiha, "tadbirkor": tadbirkor,
                        "stir": stir, "manzil": manzil, "tur": tur,
                        "qavatlar": int(qavatlar), "yer_maydoni": yer_maydoni,
                        "bosqich": bosqich, "sana": datetime.now().strftime("%Y-%m-%d"),
                        "holat": holat, "ariza_malumotlar": malumotlar,
                        "ariza_tavsif": ariza_tavsif, "rad_ariza_tavsif": rad_tavsif,
                        "organlar": org_data, "reviews": [],
                        "ai_mezon_tahlil": None, "ai_verdict": None, "_doc_sim": None,
                    })
                    save_data(apps2)
                    st.success(f"✅ Ariza **{nid}** saqlandi! AI tahlil uchun '🔍 AI Tahlil' bo'limiga o'ting.")


# ══════════════════════════════════════════════════════════════════
#  JAMOATCHILIK BAHOSI — ALOHIDA BO'LIM
# ══════════════════════════════════════════════════════════════════
elif page == "⭐  Jamoatchilik bahosi":
    st.markdown('<h1 class="glow-text">⭐ Jamoatchilik Baholash</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b">Qurilish tugallangan yoki foydalanishga topshirilgan binolarni rezidentlar, aholiqo\'shnilar va tashrif buyuruvchilar baholaydi</p>', unsafe_allow_html=True)

    apps = load_data()
    # Tasdiqlangan yoki foydalanishga topshirilgan obyektlar
    target_apps = [a for a in apps if a["holat"] in ("tasdiq", "rad_keyin_tasdiq")]

    if not target_apps:
        st.info("Tasdiqlangan yoki foydalanishga topshirilgan ariza yo'q.")
        st.stop()

    sel_id = st.selectbox(
        "Obyekt tanlang:",
        [a["id"] for a in target_apps],
        format_func=lambda x: f"{x} — {next(a['loyiha'] for a in target_apps if a['id']==x)}",
    )
    app = next(a for a in target_apps if a["id"] == sel_id)

    # Baho statistikasi
    reviews = app.get("reviews", [])
    avg_rev = np.mean([r["baho"] for r in reviews]) if reviews else 0

    st.markdown("---")

    if reviews:
        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            clr = "#ef4444" if avg_rev <= 2.5 else ("#f59e0b" if avg_rev <= 3.5 else "#10b981")
            glow = f"0 0 30px {clr}30"
            st.markdown(
                f'<div class="glass" style="border-top:4px solid {clr};text-align:center;box-shadow:{glow}">'
                f'<div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px">O\'RTACHA BAHO</div>'
                f'<div style="font-size:56px;font-weight:900;color:{clr};text-shadow:0 0 20px {clr}60;line-height:1.1">{avg_rev:.1f}</div>'
                f'<div style="font-size:22px">{"⭐" * round(avg_rev)}{"☆" * (5-round(avg_rev))}</div>'
                f'<div style="font-size:13px;color:#64748b;margin-top:8px">{len(reviews)} ta baho</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c2:
            from collections import Counter
            dist = Counter(r["baho"] for r in reviews)
            st.markdown('<b style="color:#f1f5f9">Baho taqsimoti</b>', unsafe_allow_html=True)
            st.markdown("")
            for i in range(5, 0, -1):
                cnt = dist.get(i, 0)
                bar_pct = cnt / len(reviews) if reviews else 0
                clr_b = "#ef4444" if i <= 2 else ("#f59e0b" if i == 3 else "#10b981")
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:10px;margin:5px 0">'
                    f'<span style="font-size:13px;width:80px;color:#cbd5e1">{"⭐"*i}</span>'
                    f'<div style="flex:1;height:10px;background:rgba(255,255,255,0.06);border-radius:5px;overflow:hidden">'
                    f'<div style="width:{bar_pct*100:.0f}%;height:100%;background:linear-gradient(90deg,{clr_b}88,{clr_b});border-radius:5px;transition:width 0.5s"></div></div>'
                    f'<span style="font-size:13px;color:#64748b;width:24px;text-align:right">{cnt}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Rasmiy vs aholi taqqosi
            st.markdown("")
            approved = app["holat"] in ("tasdiq", "rad_keyin_tasdiq")
            if avg_rev <= 2.5 and approved:
                st.markdown('<div class="glass-red"><b>🚨 Rasmiy xulosaga zid!</b><br><span style="font-size:12px">Aholi qoniqmaganlik bildirmoqda, ammo bino rasmiy tasdiqlangan.</span></div>', unsafe_allow_html=True)
            elif avg_rev <= 3.5 and approved:
                st.markdown('<div class="glass-yellow"><b>⚠️ Tekshiruv tavsiya</b><br><span style="font-size:12px">Baho o\'rtacha — qo\'shimcha inspeksiya buyurtma qiling.</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="glass-green"><b>✅ Aholi bahosi rasmiy xulosaga mos</b></div>', unsafe_allow_html=True)

        with c3:
            st.markdown('<b style="color:#f1f5f9">Barcha sharhlar</b>', unsafe_allow_html=True)
            for r in reversed(reviews):
                clr_r = "#ef4444" if r["baho"] <= 2 else ("#f59e0b" if r["baho"] == 3 else "#10b981")
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.03);border-left:3px solid {clr_r};'
                    f'padding:10px 14px;border-radius:0 10px 10px 0;margin:6px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<b style="font-size:13px;color:#e2e8f0">{r["ism"]}</b>'
                    f'<span style="font-size:14px">{"⭐"*r["baho"]}</span></div>'
                    f'<div style="font-size:13px;color:#94a3b8;margin-top:5px">{r["fikr"]}</div>'
                    f'<div style="font-size:11px;color:#475569;margin-top:4px">{r["sana"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.markdown('<div class="glass" style="text-align:center;padding:30px;color:#64748b">⭐ Hali baho berilmagan. Birinchi bo\'ling!</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<b style="color:#00d4ff">✍️ Baho qo\'shish</b>', unsafe_allow_html=True)

    with st.form("baho_form", clear_on_submit=True):
        fc1, fc2 = st.columns([3, 1])
        with fc1:
            fikr = st.text_area("Sizning fikringiz:", height=80,
                                 placeholder="Qurilish sifati, xavfsizlik tizimlari, infrastruktura...")
        with fc2:
            baho = st.select_slider("Baho:", options=[1, 2, 3, 4, 5], value=3,
                                     format_func=lambda x: "⭐" * x)
            ism = st.text_input("Ism:", placeholder="Anonim (ixtiyoriy)")

        if st.form_submit_button("✈️ Baho yuborish", type="primary", use_container_width=True):
            apps2 = load_data()
            for a2 in apps2:
                if a2["id"] == sel_id:
                    a2.setdefault("reviews", []).append({
                        "ism": ism.strip() or "Anonim",
                        "baho": baho,
                        "fikr": fikr,
                        "sana": datetime.now().strftime("%Y-%m-%d"),
                    })
            save_data(apps2)
            st.success("✅ Rahmat! Sizning bahongiz qo'shildi.")
            st.rerun()


# ══════════════════════════════════════════════════════════════════
#  STATISTIKA
# ══════════════════════════════════════════════════════════════════
elif page == "📊  Statistika":
    st.markdown('<h1 class="glow-text">📊 Umumiy Statistika</h1>', unsafe_allow_html=True)
    apps = load_data()

    rows = []
    for a in apps:
        m = ai_score_from_data(a.get("ariza_malumotlar", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        t1, t2 = a.get("rad_ariza_tavsif", ""), a.get("ariza_tavsif", "")
        dsim = 0
        if rad_bor and t1 and t2:
            w1, w2 = set(t1.lower().split()), set(t2.lower().split())
            dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(m["pct"], dsim, avg, a["holat"], rad_bor, revs)
        rows.append({**a, "pct": m["pct"], "dsim": dsim, "avg": avg, "vscore": v["score"], "vlevel": v["level"]})

    red_r = [r for r in rows if r["vscore"] >= 50]
    yel_r = [r for r in rows if 20 <= r["vscore"] < 50]

    cols = st.columns(5)
    for i, (lab, val, clr) in enumerate([
        ("JAMI ARIZALAR", len(rows), "#00d4ff"),
        ("🔴 YUQORI XAVF", len(red_r), "#ef4444"),
        ("🟡 O'RTA XAVF", len(yel_r), "#f59e0b"),
        ("🟢 PAST XAVF", len(rows)-len(red_r)-len(yel_r), "#10b981"),
        ("⚠️ RAD→TASDIQ", len([a for a in apps if a["holat"] == "rad_keyin_tasdiq"]), "#a855f7"),
    ]):
        cols[i].markdown(
            f'<div class="kpi-glass">'
            f'<div class="kpi-val" style="color:{clr};text-shadow:0 0 15px {clr}30">{val}</div>'
            f'<div class="kpi-lab">{lab}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<b style="color:#f1f5f9;font-size:17px">Xavf darajasi jadvali</b>', unsafe_allow_html=True)

    hdr = st.columns([2, 3, 1, 1, 1, 1])
    for col, txt in zip(hdr, ["ID", "Loyiha", "VMQ%", "Hujjat%", "Baho", "Xavf"]):
        col.markdown(f'<span style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px">{txt}</span>', unsafe_allow_html=True)

    for r in sorted(rows, key=lambda x: -x["vscore"]):
        icon = "🔴" if r["vscore"] >= 50 else ("🟡" if r["vscore"] >= 20 else "🟢")
        rc = st.columns([2, 3, 1, 1, 1, 1])
        rc[0].markdown(f'<span style="color:#00d4ff;font-weight:700">{r["id"]}</span>', unsafe_allow_html=True)
        rc[1].write(r["loyiha"][:30])
        rc[2].write(f"{r['pct']:.0f}%")
        rc[3].write(f"{r['dsim']:.0f}%" if r["holat"] == "rad_keyin_tasdiq" else "—")
        rc[4].write(f"{r['avg']:.1f}⭐" if r.get("reviews") else "—")
        rc[5].write(f"{icon} {r['vscore']}")

    st.markdown("---")
    st.markdown('<b style="color:#f1f5f9;font-size:17px">Bo\'limlar bo\'yicha o\'rtacha VMQ mezon muvofiqlik</b>', unsafe_allow_html=True)

    dept_avgs = {"🧪 Sanitariya": [], "🔥 Yong'in": [], "🌿 Ekologiya": [], "🏗️ Qurilish": []}
    for a in apps:
        m = ai_score_from_data(a.get("ariza_malumotlar", {}))
        for dept, pct in m["dept_pct"].items():
            if dept in dept_avgs:
                dept_avgs[dept].append(pct)

    dc = st.columns(4)
    for i, (dept, vals) in enumerate(dept_avgs.items()):
        avg_d = np.mean(vals) if vals else 0
        clr = "#ef4444" if avg_d < 60 else ("#f59e0b" if avg_d < 75 else "#10b981")
        dc[i].markdown(
            f'<div class="metric-glass" style="border-top:3px solid {clr}">'
            f'<div style="font-size:12px;color:#94a3b8;margin-bottom:6px">{dept}</div>'
            f'<div style="font-size:30px;font-weight:800;color:{clr}">{avg_d:.0f}%</div>'
            f'</div>', unsafe_allow_html=True,
        )
        dc[i].progress(avg_d / 100)
