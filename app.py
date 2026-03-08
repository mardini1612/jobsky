import streamlit as st
import requests
import PyPDF2
from PIL import Image
import io
import base64
import time

OPENROUTER_API_KEY = "AIzaSyAJa-ev3_uh8CJqY7odjC_47FfVh_pGuXQ"

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + OPENROUTER_API_KEY},
            json={
                "model": "gemini-1.5-flash",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return "خطأ: " + str(data)
    except Exception as e:
        return "خطأ: " + str(e)

st.set_page_config(page_title="JobSky", page_icon="☁️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
* { font-family: 'Cairo', sans-serif !important; direction: rtl; box-sizing: border-box; }
html, body, .stApp { background: #000000 !important; color: #e0f0ff !important; }
.stApp { background: radial-gradient(ellipse at 20% 20%, rgba(0,50,150,0.15) 0%, transparent 50%), #000000 !important; }
.logo-wrap { text-align:center; padding: 50px 0 5px 0; }
.logo-text { font-size: 80px; font-weight: 900; letter-spacing: 10px; background: linear-gradient(135deg, #0077ff, #00ccff, #0055dd, #00aaff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: inline-block; animation: logoBreath 2.5s ease-in-out infinite; }
@keyframes logoBreath { 0% { filter: brightness(0.35) drop-shadow(0 0 4px #0044ff); opacity: 0.45; } 50% { filter: brightness(1.4) drop-shadow(0 0 35px #00aaff) drop-shadow(0 0 70px #0055ff); opacity: 1; } 100% { filter: brightness(0.35) drop-shadow(0 0 4px #0044ff); opacity: 0.45; } }
.logo-cloud { font-size: 55px; display: inline-block; animation: cloudPulse 2.5s ease-in-out infinite; margin-left: 10px; }
@keyframes cloudPulse { 0%, 100% { transform: translateY(2px); filter: drop-shadow(0 0 8px #0077ff); opacity: 0.5; } 50% { transform: translateY(-6px); filter: drop-shadow(0 0 30px #00ccff); opacity: 1; } }
.slogan { text-align: center; color: #6699cc !important; font-size: 16px !important; letter-spacing: 3px; margin: 8px 0 35px 0; animation: sloganFade 2.5s ease-in-out infinite; }
@keyframes sloganFade { 0%, 100% { opacity: 0.4; } 50% { opacity: 0.9; } }
.stats-row { display: flex; justify-content: center; gap: 20px; margin: 10px 0 40px 0; flex-wrap: wrap; }
.stat-box { background: linear-gradient(145deg, rgba(0,40,100,0.45), rgba(0,15,50,0.7)); border: 1px solid rgba(0,120,255,0.25); border-radius: 18px; padding: 18px 28px; text-align: center; min-width: 120px; animation: boxGlow 3s ease-in-out infinite; }
.stat-box:nth-child(2) { animation-delay: 0.8s; }
.stat-box:nth-child(3) { animation-delay: 1.6s; }
@keyframes boxGlow { 0%, 100% { border-color: rgba(0,80,200,0.2); box-shadow: 0 0 8px rgba(0,80,200,0.08); } 50% { border-color: rgba(0,180,255,0.6); box-shadow: 0 0 25px rgba(0,140,255,0.25); } }
.stat-num { font-size: 32px; font-weight: 900; background: linear-gradient(135deg, #0099ff, #00ddff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-lbl { font-size: 11px; color: #557799 !important; margin-top: 3px; }
.gdiv { height: 1px; background: linear-gradient(90deg, transparent, #0066ff, #00ccff, #0066ff, transparent); margin: 25px 0; animation: gdivGlow 3s ease-in-out infinite; }
@keyframes gdivGlow { 0%, 100% { opacity: 0.25; } 50% { opacity: 0.9; } }
.sec-title { text-align: center; font-size: 20px !important; font-weight: 700 !important; color: #88bbdd !important; margin: 25px 0 18px 0; letter-spacing: 1px; }
[data-testid="stFileUploader"] { background: linear-gradient(145deg, rgba(0,25,70,0.5), rgba(0,8,35,0.8)) !important; border: 2px solid rgba(0,110,255,0.35) !important; border-radius: 22px !important; padding: 8px !important; animation: uploaderGlow 2.5s ease-in-out infinite !important; }
@keyframes uploaderGlow { 0%, 100% { border-color: rgba(0,80,200,0.25); box-shadow: 0 0 12px rgba(0,80,200,0.1); } 50% { border-color: rgba(0,170,255,0.65); box-shadow: 0 0 30px rgba(0,130,255,0.3); } }
[data-testid="stFileDropzone"] { background: transparent !important; border: none !important; }
.stButton > button { background: linear-gradient(135deg, #002288, #0055ee, #0088ff) !important; color: #ffffff !important; border: none !important; border-radius: 60px !important; padding: 15px 40px !important; font-size: 17px !important; font-weight: 800 !important; font-family: 'Cairo', sans-serif !important; width: 100% !important; letter-spacing: 2px; animation: btnPulse 2.5s ease-in-out infinite !important; transition: transform 0.2s !important; }
@keyframes btnPulse { 0%, 100% { box-shadow: 0 0 12px rgba(0,80,220,0.4); } 50% { box-shadow: 0 0 35px rgba(0,160,255,0.75), 0 0 70px rgba(0,80,200,0.25); } }
.anime-wrap { display: flex; flex-direction: column; align-items: center; padding: 25px 0; }
.anime-emoji { font-size: 85px; filter: drop-shadow(0 0 20px rgba(0,150,255,0.7)); margin-bottom: 10px; }
.speech-bubble { background: linear-gradient(135deg, rgba(0,25,70,0.92), rgba(0,10,45,0.95)); border: 2px solid rgba(0,130,255,0.5); border-radius: 22px; padding: 14px 28px; max-width: 380px; text-align: center; color: #99ccee !important; font-size: 15px; font-weight: 600; animation: bubblePulse 1.5s ease-in-out infinite; }
@keyframes bubblePulse { 0%, 100% { box-shadow: 0 0 8px rgba(0,100,200,0.2); } 50% { box-shadow: 0 0 22px rgba(0,150,255,0.5); } }
.result-wrap { background: linear-gradient(145deg, rgba(0,18,55,0.92), rgba(0,8,35,0.97)); border: 2px solid rgba(0,140,255,0.45); border-radius: 26px; padding: 28px; margin: 18px 0; box-shadow: 0 0 35px rgba(0,90,200,0.18); animation: resultIn 0.4s ease-out; }
@keyframes resultIn { from { opacity:0; transform: translateY(18px); } to { opacity:1; transform: translateY(0); } }
.offer-wrap { background: linear-gradient(145deg, rgba(0,50,25,0.6), rgba(0,25,12,0.85)); border: 2px solid rgba(0,230,90,0.35); border-radius: 26px; padding: 28px; margin: 18px 0; text-align: center; animation: offerGlow 2s ease-in-out infinite; }
@keyframes offerGlow { 0%, 100% { border-color: rgba(0,180,70,0.25); box-shadow: 0 0 12px rgba(0,180,70,0.08); } 50% { border-color: rgba(0,255,110,0.65); box-shadow: 0 0 35px rgba(0,240,100,0.25); } }
.price { font-size: 50px; font-weight: 900; background: linear-gradient(135deg, #00ff88, #00ccff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.feat-tag { display: inline-block; background: rgba(0,90,40,0.35); border: 1px solid rgba(0,200,80,0.3); border-radius: 50px; padding: 7px 18px; margin: 5px 4px; color: #88ffbb !important; font-size: 13px; font-weight: 600; }
.build-title { font-size: 24px; font-weight: 900; background: linear-gradient(135deg, #00ff88, #0099ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: inline-block; animation: logoBreath 2.5s ease-in-out infinite; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
p, span, div, label { color: #b0cce0 !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #0044cc; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-wrap">
    <span class="logo-cloud">☁️</span>
    <span class="logo-text">JobSky</span>
</div>
<p class="slogan">✦ ابني سيرتك الذكية بنظام ATS ✦</p>
<div class="gdiv"></div>
<div class="stats-row">
    <div class="stat-box"><div class="stat-num">+٢٤٠٠</div><div class="stat-lbl">سيرة مفحوصة</div></div>
    <div class="stat-box"><div class="stat-num">٨٩٪</div><div class="stat-lbl">نسبة القبول</div></div>
    <div class="stat-box"><div class="stat-num">+٥٠٠</div><div class="stat-lbl">عميل راضٍ</div></div>
</div>
<div class="gdiv"></div>
""", unsafe_allow_html=True)

st.markdown('<p class="sec-title">📄 ارفع سيرتك الذاتية للفحص المجاني</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("اسحب ملفك هنا أو اضغط للاختيار", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    st.markdown("<div style='text-align:center; margin:12px 0; padding:12px 20px; background:rgba(0,40,90,0.45); border-radius:14px; border:1px solid rgba(0,140,255,0.35);'><span style='color:#00ccff; font-size:15px; font-weight:700;'>✅ " + uploaded_file.name + "</span></div>", unsafe_allow_html=True)

    cv_text = ""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            cv_text += page.extract_text()
    else:
        image = Image.open(uploaded_file)
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        cv_text = ask_ai("استخرج كل النص من هذه السيرة الذاتية")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍   افحص سيرتي الآن مجاناً"):
        anime_spot = st.empty()
        stages = [
            ("🧑‍💻", "أراجع سيرتك الذاتية..."),
            ("📋", "أفحص التنسيق والهيكل..."),
            ("🔍", "أبحث عن الكلمات المفتاحية..."),
            ("😤", "هممم... أرى مشاكل واضحة!"),
            ("✍️", "أكتب تقرير الفحص..."),
            ("😏", "واضح ما المشكلة... سأصلحها!"),
            ("😊", "انتهيت! تفضّل نتيجتك ☁️"),
        ]
        for emoji, msg in stages:
            anime_spot.markdown("<div class='anime-wrap'><div class='anime-emoji'>" + emoji + "</div><div class='speech-bubble'>" + msg + "</div></div>", unsafe_allow_html=True)
            time.sleep(1.3)
        anime_spot.empty()

        prompt = "أنت خبير موارد بشرية متخصص في أنظمة ATS العالمية والسعودية.\nافحص هذه السيرة الذاتية بدقة واعطني بالعربية فقط:\n\nالنسبة: XX%\nالسبب الأول: ...\nالسبب الثاني: ...\nالسبب الثالث: ...\nالخلاصة: جملة واحدة صادمة وصادقة\n\nالسيرة:\n" + cv_text

        result = ask_ai(prompt)

        st.markdown("<div class='result-wrap'><p style='text-align:center; font-size:19px; font-weight:800; color:#88bbdd; margin-bottom:20px; letter-spacing:2px;'>📊 نتيجة الفحص الذكي</p><div style='font-size:16px; line-height:2.4; color:#cce8ff !important; white-space:pre-wrap; text-align:right;'>" + result + "</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='gdiv'></div>", unsafe_allow_html=True)

        st.markdown("""<div class='offer-wrap'>
            <div style='font-size:20px; font-weight:800; color:#aaffcc !important; margin-bottom:12px;'>🚀 حسّن سيرتك واحصل على وظيفة أحلامك</div>
            <div class='price'>٢٢ ريال</div>
            <div style='color:#557766 !important; font-size:13px; margin:8px 0 18px 0;'>بدلاً من ٢٠٠+ ريال في مراكز التوظيف</div>
            <div>
                <span class='feat-tag'>✅ سيرة عربية</span>
                <span class='feat-tag'>✅ سيرة إنجليزية</span>
                <span class='feat-tag'>✅ PDF</span>
                <span class='feat-tag'>✅ Word</span>
                <span class='feat-tag'>✅ ATS 100٪</span>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("⚡   احصل على سيرتك المحسّنة - ٢٢ ريال"):
            st.markdown("<div style='text-align:center; padding:18px; background:rgba(0,40,20,0.5); border-radius:16px; border:1px solid rgba(0,230,90,0.3); margin:10px 0;'><span style='color:#00ff88 !important; font-size:17px; font-weight:700;'>✅ سيتم تحويلك لصفحة الدفع الآمنة</span></div>", unsafe_allow_html=True)

st.markdown("<div class='gdiv'></div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; margin:25px 0 12px 0;'><span class='build-title'>✨ ابنِ سيرتك الذاتية من الصفر</span><p style='color:#445566 !important; font-size:14px; margin-top:6px;'>لا تملك سيرة؟ نبنيها لك باحترافية عالية</p></div>", unsafe_allow_html=True)

if st.button("🌟   ابنِ سيرتك الذاتية الآن"):
    st.markdown("<div style='text-align:center; padding:16px; background:rgba(0,15,50,0.6); border-radius:16px; border:1px solid rgba(0,120,255,0.35); margin:10px 0;'><span style='color:#88aadd !important; font-size:15px; font-weight:700;'>🔜 ميزة قادمة قريباً!</span></div>", unsafe_allow_html=True)

st.markdown("<div class='gdiv'></div><div style='text-align:center; padding:15px 0 35px 0;'><span style='color:#223344 !important; font-size:12px;'>☁️ JobSky - جميع الحقوق محفوظة ٢٠٢٥</span></div>", unsafe_allow_html=True)
