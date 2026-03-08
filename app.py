import streamlit as st
import google.generativeai as genai
import PyPDF2
from PIL import Image
import time

genai.configure(api_key="AIzaSyAJa-ev3_uh8CJqY7odjC_47FfVh_pGuXQ")

def ask_ai(prompt, image=None):
try:
model = genai.GenerativeModel(“gemini-1.5-flash”)
if image:
response = model.generate_content([prompt, image])
else:
response = model.generate_content(prompt)
return response.text
except Exception as e:
return “خطأ: “ + str(e)

st.set_page_config(page_title=“JobSky”, page_icon=“☁️”, layout=“centered”)

st.markdown(”””

<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
* { font-family: 'Cairo', sans-serif !important; direction: rtl; box-sizing: border-box; }
html, body, .stApp { background: #000000 !important; color: #e0f0ff !important; }
.logo-text { font-size: 80px; font-weight: 900; letter-spacing: 10px; background: linear-gradient(135deg, #0077ff, #00ccff, #0055dd, #00aaff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: inline-block; animation: logoBreath 2.5s ease-in-out infinite; }
@keyframes logoBreath { 0% { filter: brightness(0.35) drop-shadow(0 0 4px #0044ff); opacity: 0.45; } 50% { filter: brightness(1.4) drop-shadow(0 0 35px #00aaff) drop-shadow(0 0 70px #0055ff); opacity: 1; } 100% { filter: brightness(0.35) drop-shadow(0 0 4px #0044ff); opacity: 0.45; } }
.logo-cloud { font-size: 55px; display: inline-block; animation: cloudPulse 2.5s ease-in-out infinite; margin-left: 10px; }
@keyframes cloudPulse { 0%, 100% { transform: translateY(2px); filter: drop-shadow(0 0 8px #0077ff); opacity: 0.5; } 50% { transform: translateY(-6px); filter: drop-shadow(0 0 30px #00ccff); opacity: 1; } }
.slogan { text-align: center; color: #6699cc !important; font-size: 16px !important; letter-spacing: 3px; margin: 8px 0 35px 0; }
@keyframes dominoDown { from { opacity: 0; transform: translateY(-60px); } to { opacity: 1; transform: translateY(0); } }
@keyframes dominoUp { from { opacity: 0; transform: translateY(60px); } to { opacity: 1; transform: translateY(0); } }
.d-down { animation: dominoDown 0.5s ease-out both; }
.d-up { animation: dominoUp 0.5s ease-out both; }
.dl1{animation-delay:0.0s}.dl2{animation-delay:0.15s}.dl3{animation-delay:0.30s}.dl4{animation-delay:0.45s}.dl5{animation-delay:0.60s}.dl6{animation-delay:0.75s}
.stats-row { display: flex; justify-content: center; gap: 20px; margin: 10px 0 40px 0; flex-wrap: wrap; }
.stat-box { background: linear-gradient(145deg, rgba(0,40,100,0.45), rgba(0,15,50,0.7)); border: 1px solid rgba(0,120,255,0.25); border-radius: 18px; padding: 18px 28px; text-align: center; min-width: 120px; }
.stat-num { font-size: 32px; font-weight: 900; background: linear-gradient(135deg, #0099ff, #00ddff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-lbl { font-size: 11px; color: #557799 !important; margin-top: 3px; }
.gdiv { height: 1px; background: linear-gradient(90deg, transparent, #0066ff, #00ccff, #0066ff, transparent); margin: 25px 0; opacity: 0.4; }
.stButton > button { background: linear-gradient(135deg, #002288, #0055ee, #0088ff) !important; color: #ffffff !important; border: none !important; border-radius: 60px !important; padding: 15px 40px !important; font-size: 17px !important; font-weight: 800 !important; font-family: 'Cairo', sans-serif !important; width: 100% !important; letter-spacing: 2px; transition: transform 0.2s !important; }
.stButton > button:hover { transform: scale(1.02) !important; }
.glow-btn .stButton > button { animation: btnPulse 2.5s ease-in-out infinite !important; }
@keyframes btnPulse { 0%, 100% { box-shadow: 0 0 12px rgba(0,80,220,0.4); } 50% { box-shadow: 0 0 35px rgba(0,160,255,0.75), 0 0 70px rgba(0,80,200,0.25); } }
.anime-wrap { display: flex; flex-direction: column; align-items: center; padding: 25px 0; }
.anime-emoji { font-size: 85px; filter: drop-shadow(0 0 20px rgba(0,150,255,0.7)); margin-bottom: 10px; }
.speech-bubble { background: linear-gradient(135deg, rgba(0,25,70,0.92), rgba(0,10,45,0.95)); border: 2px solid rgba(0,130,255,0.5); border-radius: 22px; padding: 14px 28px; max-width: 380px; text-align: center; color: #99ccee !important; font-size: 15px; font-weight: 600; }
.result-wrap { background: linear-gradient(145deg, rgba(0,18,55,0.92), rgba(0,8,35,0.97)); border: 2px solid rgba(0,140,255,0.45); border-radius: 26px; padding: 28px; margin: 18px 0; animation: resultIn 0.4s ease-out; }
@keyframes resultIn { from { opacity:0; transform: translateY(18px); } to { opacity:1; transform: translateY(0); } }
.offer-wrap { background: linear-gradient(145deg, rgba(0,50,25,0.6), rgba(0,25,12,0.85)); border: 2px solid rgba(0,230,90,0.35); border-radius: 26px; padding: 28px; margin: 18px 0; text-align: center; }
.price { font-size: 50px; font-weight: 900; background: linear-gradient(135deg, #00ff88, #00ccff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.feat-tag { display: inline-block; background: rgba(0,90,40,0.35); border: 1px solid rgba(0,200,80,0.3); border-radius: 50px; padding: 7px 18px; margin: 5px 4px; color: #88ffbb !important; font-size: 13px; font-weight: 600; }
.build-title { font-size: 26px; font-weight: 900; background: linear-gradient(135deg, #00ff88, #0099ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: inline-block; animation: logoBreath 2.5s ease-in-out infinite; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: rgba(0,20,60,0.7) !important; border: 1px solid rgba(0,120,255,0.4) !important; border-radius: 12px !important; color: #c0e0ff !important; font-family: 'Cairo', sans-serif !important; font-size: 15px !important; }
.stSelectbox > div > div { background: rgba(0,20,60,0.7) !important; border: 1px solid rgba(0,120,255,0.4) !important; border-radius: 12px !important; color: #c0e0ff !important; }
label { color: #88bbdd !important; font-weight: 600 !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
p, span, div { color: #b0cce0 !important; }
</style>

“””, unsafe_allow_html=True)

st.markdown(”””

<div style="text-align:center; padding: 50px 0 5px 0;" class="d-down dl1">
    <span class="logo-cloud">☁️</span>
    <span class="logo-text">JobSky</span>
</div>
<p class="slogan d-down dl2">✦ ابني سيرتك الذكية بنظام ATS ✦</p>
<div class="gdiv d-down dl3"></div>
<div class="stats-row d-down dl4">
    <div class="stat-box"><div class="stat-num">+2400</div><div class="stat-lbl">سيرة مفحوصة</div></div>
    <div class="stat-box"><div class="stat-num">89%</div><div class="stat-lbl">نسبة القبول</div></div>
    <div class="stat-box"><div class="stat-num">+500</div><div class="stat-lbl">عميل راضٍ</div></div>
</div>
<div class="gdiv d-down dl5"></div>
<p style="text-align:center;font-size:20px;font-weight:700;color:#88bbdd;margin:25px 0 18px 0;" class="d-down dl6">📄 ارفع سيرتك الذاتية للفحص المجاني</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(“اسحب ملفك هنا او اضغط للاختيار”, type=[“pdf”, “png”, “jpg”, “jpeg”])

if uploaded_file:
st.markdown(”<div style='text-align:center;margin:12px 0;padding:12px 20px;background:rgba(0,40,90,0.45);border-radius:14px;border:1px solid rgba(0,140,255,0.35);'><span style='color:#00ccff;font-size:15px;font-weight:700;'>✅ “ + uploaded_file.name + “</span></div>”, unsafe_allow_html=True)
cv_text = “”
cv_image = None
if uploaded_file.type == “application/pdf”:
pdf_reader = PyPDF2.PdfReader(uploaded_file)
for page in pdf_reader.pages:
cv_text += page.extract_text()
else:
cv_image = Image.open(uploaded_file)
st.image(cv_image, width=200)

```
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
check_btn = st.button("🔍   افحص سيرتي الآن مجانا")
st.markdown("</div>", unsafe_allow_html=True)

if check_btn:
    anime_spot = st.empty()
    stages = [("🧑‍💻","اراجع سيرتك..."),("📋","افحص التنسيق..."),("🔍","ابحث عن الكلمات المفتاحية..."),("😤","ارى مشاكل واضحة!"),("✍️","اكتب التقرير..."),("😏","واضح المشكلة!"),("😊","انتهيت! ☁️")]
    for emoji, msg in stages:
        anime_spot.markdown("<div class='anime-wrap'><div class='anime-emoji'>" + emoji + "</div><div class='speech-bubble'>" + msg + "</div></div>", unsafe_allow_html=True)
        time.sleep(1.3)
    anime_spot.empty()
    prompt = "انت خبير موارد بشرية متخصص في انظمة ATS السعودية. افحص هذه السيرة واعطني بالعربية:\nالنسبة: XX%\nالسبب الاول: ...\nالسبب الثاني: ...\nالسبب الثالث: ...\nالخلاصة: جملة واحدة\n\nالسيرة:\n" + cv_text
    if cv_image:
        result = ask_ai("انت خبير ATS. افحص السيرة في الصورة بالعربية:\nالنسبة: XX%\nالسبب الاول: ...\nالسبب الثاني: ...\nالسبب الثالث: ...\nالخلاصة: جملة واحدة", cv_image)
    else:
        result = ask_ai(prompt)
    st.markdown("<div class='result-wrap'><p style='text-align:center;font-size:19px;font-weight:800;color:#88bbdd;margin-bottom:20px;'>📊 نتيجة الفحص الذكي</p><div style='font-size:16px;line-height:2.4;color:#cce8ff !important;white-space:pre-wrap;text-align:right;'>" + result + "</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='offer-wrap'><div style='font-size:20px;font-weight:800;color:#aaffcc !important;margin-bottom:12px;'>🚀 حسّن سيرتك واحصل على وظيفة احلامك</div><div class='price'>22 ريال</div><div style='color:#557766 !important;font-size:13px;margin:8px 0 18px 0;'>بدلاً من 200+ ريال في مراكز التوظيف</div><div><span class='feat-tag'>✅ سيرة عربية</span><span class='feat-tag'>✅ سيرة انجليزية</span><span class='feat-tag'>✅ PDF</span><span class='feat-tag'>✅ Word</span><span class='feat-tag'>✅ ATS 100%</span></div></div>", unsafe_allow_html=True)
    if st.button("⚡   احصل على سيرتك المحسّنة - 22 ريال"):
        st.markdown("<div style='text-align:center;padding:18px;background:rgba(0,40,20,0.5);border-radius:16px;'><span style='color:#00ff88 !important;font-size:17px;font-weight:700;'>✅ سيتم تحويلك لصفحة الدفع</span></div>", unsafe_allow_html=True)
```

st.markdown(”<div class='gdiv d-up dl1'></div>”, unsafe_allow_html=True)
st.markdown(”<div style='text-align:center;margin:25px 0 12px 0;' class='d-up dl2'><span class='build-title'>✨ ابنِ سيرتك الذاتية من الصفر</span><p style='color:#445566 !important;font-size:14px;margin-top:6px;'>لا تملك سيرة؟ نبنيها لك باحترافية خلال دقائق</p></div>”, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
full_name = st.text_input(“الاسم الكامل”, placeholder=“محمد عبدالله الاحمدي”)
phone = st.text_input(“رقم الجوال”, placeholder=“05xxxxxxxx”)
city = st.text_input(“المدينة”, placeholder=“الرياض”)
with col2:
email = st.text_input(“البريد الالكتروني”, placeholder=“example@gmail.com”)
job_title = st.text_input(“المسمى الوظيفي”, placeholder=“مهندس برمجيات”)
years_exp = st.selectbox(“سنوات الخبرة”, [“بدون خبرة”, “1-2 سنة”, “3-5 سنوات”, “6-10 سنوات”, “اكثر من 10”])

education = st.text_input(“المؤهل العلمي”, placeholder=“بكالوريوس علوم حاسب - جامعة الملك سعود 2022”)
skills = st.text_area(“المهارات”, placeholder=“Python, Excel, ادارة المشاريع…”, height=80)
experience = st.text_area(“الخبرات السابقة”, placeholder=“مطور ويب في شركة STC لمدة سنتين…”, height=100)

st.markdown(”<br>”, unsafe_allow_html=True)
st.markdown(’<div class="glow-btn d-up dl3">’, unsafe_allow_html=True)
build_btn = st.button(“🌟   ابنِ سيرتي الذكية الآن”)
st.markdown(”</div>”, unsafe_allow_html=True)

if build_btn:
if not full_name or not job_title:
st.warning(“يرجى ادخال الاسم والمسمى الوظيفي”)
else:
anime_spot2 = st.empty()
stages2 = [(“🧑‍💻”,“اراجع معلوماتك…”),(“✍️”,“اكتب سيرتك…”),(“🌍”,“اترجمها للانجليزية…”),(“✨”,“اضيف اللمسات الاحترافية…”),(“😊”,“سيرتك جاهزة! ☁️”)]
for emoji, msg in stages2:
anime_spot2.markdown(”<div class='anime-wrap'><div class='anime-emoji'>” + emoji + “</div><div class='speech-bubble'>” + msg + “</div></div>”, unsafe_allow_html=True)
time.sleep(1.3)
anime_spot2.empty()
prompt_build = “انت خبير كتابة سير ذاتية للسوق السعودي ومتخصص في ATS. اكتب سيرة ذاتية احترافية متكاملة بالعربية للشخص التالي:\nالاسم: “ + full_name + “\nالبريد: “ + email + “\nالجوال: “ + phone + “\nالمدينة: “ + city + “\nالمسمى: “ + job_title + “\nالخبرة: “ + years_exp + “\nالتعليم: “ + education + “\nالمهارات: “ + skills + “\nالخبرات: “ + experience
result_cv = ask_ai(prompt_build)
st.markdown(”<div class='result-wrap'><p style='text-align:center;font-size:19px;font-weight:800;color:#88bbdd;margin-bottom:20px;'>✨ سيرتك الذاتية الاحترافية</p><div style='font-size:15px;line-height:2.2;color:#cce8ff !important;white-space:pre-wrap;text-align:right;'>” + result_cv + “</div></div>”, unsafe_allow_html=True)
st.markdown(”<div class='offer-wrap'><div style='font-size:18px;font-weight:800;color:#aaffcc !important;margin-bottom:12px;'>🚀 احصل على نسختك PDF و Word</div><div class='price'>22 ريال</div><div><span class='feat-tag'>✅ PDF جاهز</span><span class='feat-tag'>✅ Word قابل للتعديل</span><span class='feat-tag'>✅ عربي + انجليزي</span></div></div>”, unsafe_allow_html=True)
if st.button(“⚡   احصل على ملفاتك - 22 ريال”):
st.markdown(”<div style='text-align:center;padding:18px;background:rgba(0,40,20,0.5);border-radius:16px;'><span style='color:#00ff88 !important;font-size:17px;font-weight:700;'>✅ سيتم تحويلك لصفحة الدفع</span></div>”, unsafe_allow_html=True)

st.markdown(”<div class='gdiv d-up dl4'></div>”, unsafe_allow_html=True)
st.markdown(”<div style='text-align:center;padding:15px 0 35px 0;' class='d-up dl5'><span style='color:#223344 !important;font-size:12px;'>☁️ JobSky - جميع الحقوق محفوظة 2026</span></div>”, unsafe_allow_html=True)
