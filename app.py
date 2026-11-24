from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import os
import uuid
# ==================== 1. Security (Fixed) ====================
KEY_FILE = "license.key"

def get_machine_id():
    return hex(uuid.getnode())

def generate_password(mid):
    # مطابقة تامة لمنطق أداة فك الحماية الثابتة
    digits = ''.join(filter(str.isdigit, mid))
    if not digits: 
        try:
            digits = str(int(mid, 16))
        except:
            return "Error"
    num = int(digits)
    result = round(abs(num / 2 * 3.14))
    return str(result)[:6]

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = os.path.exists(KEY_FILE)

if not st.session_state['authenticated']:
    st.set_page_config(page_title="Security", layout="centered")
    st.title("Security Activation - Ask the programmer for your password")
    st.warning("Send your Machine ID to programmer email : mulham81ahmed@gmail.com ")

    mid = get_machine_id()
    st.info(f"Machine ID: {mid}")
    pwd = st.text_input("Enter Activation Key:", type="password")
    
    if st.button("Activate"):
        if pwd == generate_password(mid):
            with open(KEY_FILE, "w") as f: 
                f.write(pwd)
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid Activation Key.")
            
    st.stop()

st.set_page_config(
    page_title="اسأل استرو رادار",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HTML_FILENAME = "Full_ask_astro_radar.html"

DEVICE_PROFILES = {
    "كمبيوتر": {"width": "100%", "height": 1220, "max_width": "100%"},
    "تابلت": {"width": "820px", "height": 1260, "max_width": "820px"},
    "مبايل": {"width": "410px", "height": 1340, "max_width": "410px"},
}


def load_html_file(filename: str) -> str | None:
    """يبحث عن ملف العرض ويعيد محتواه دون كشف اسمه في الواجهة."""
    base_dir = Path(__file__).resolve().parent
    candidate_paths = [
        base_dir / filename,
        Path.cwd() / filename,
        base_dir / "assets" / filename,
        base_dir / "static" / filename,
    ]
    for path in candidate_paths:
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8")

    for match in base_dir.rglob(filename):
        if match.is_file():
            return match.read_text(encoding="utf-8")

    return None


html_content = load_html_file(HTML_FILENAME)

if "device_mode" not in st.session_state:
    st.session_state.device_mode = "كمبيوتر"

if "reload_nonce" not in st.session_state:
    st.session_state.reload_nonce = 0

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800&display=swap');

      html, body, [class*="css"], .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', 'Tajawal', sans-serif;
      }

      /* خلفية بنفسجية غامقة متدرجة */
      .stApp {
        background: radial-gradient(circle at 18% 10%, #2a1042 0%, #140724 55%, #0b0314 100%) !important;
        color: #f8fafc;
      }

      .block-container {
        padding-top: 0.65rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        max-width: 100% !important;
      }

      header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.2rem !important;
      }

      .radar-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        background: linear-gradient(135deg, rgba(34, 12, 58, 0.95), rgba(20, 7, 36, 0.95));
        border: 1px solid rgba(253, 230, 138, 0.28);
        border-radius: 14px;
        padding: 10px 16px;
        margin-bottom: 10px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.55);
      }

      .radar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .radar-dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background: #fde68a;
        box-shadow: 0 0 12px #fde68a;
      }

      .radar-title {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 800;
        color: #fde68a;
      }

      .radar-sub {
        margin: 0;
        font-size: 0.82rem;
        color: #d8b4fe;
        font-weight: 600;
      }

      .radar-badge {
        background: rgba(126, 34, 206, 0.25);
        border: 1px solid rgba(216, 180, 254, 0.4);
        color: #f3e8ff;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
      }

      div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(125, 211, 252, 0.35) !important;
        border-radius: 10px !important;
        font-family: 'Cairo', 'Tajawal', sans-serif !important;
        font-weight: 700 !important;
        padding: 0.42rem 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.28) !important;
      }

      div.stButton > button:hover {
        transform: translateY(-1px);
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        border-color: #fde68a !important;
      }

      /* تنسيق أزرار اختيار الجهاز (مبايل - كمبيوتر - تابلت) */
      div[data-testid="stRadio"] > div {
        background: rgba(34, 12, 58, 0.75);
        border: 1px solid rgba(216, 180, 254, 0.25);
        border-radius: 12px;
        padding: 4px 10px;
        gap: 10px;
      }

      div[data-testid="stRadio"] label p {
        color: #f3e8ff !important;
        font-weight: 700 !important;
        font-family: 'Cairo', 'Tajawal', sans-serif !important;
      }

      .astro-frame-outer {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 6px;
      }

      .astro-frame-wrap {
        background: #1b0930;
        border: 1px solid rgba(253, 230, 138, 0.25);
        border-radius: 16px;
        padding: 6px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.65);
        transition: all 0.25s ease;
      }

      iframe {
        border-radius: 12px !important;
        background: #edf1ee;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="radar-topbar">
      <div class="radar-brand">
        <span class="radar-dot"></span>
        <div>
          <p class="radar-title">اسأل استرو رادار</p>
          <p class="radar-sub">تصميم الفلكي استرو رادار</p>
        </div>
      </div>
      <span class="radar-badge">شاشة كاملة</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col_mode, col_refresh = st.columns([4.2, 1.2])

with col_mode:
    selected_device = st.radio(
        "وضع العرض",
        options=["مبايل", "كمبيوتر", "تابلت"],
        index=["مبايل", "كمبيوتر", "تابلت"].index(st.session_state.device_mode),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.device_mode = selected_device

with col_refresh:
    if st.button("🔄 تحديث العرض", use_container_width=True):
        st.session_state.reload_nonce += 1
        st.rerun()

if html_content is None:
    st.error("تعذر العثور على مصدر العرض في مجلد التطبيق الحالي. يرجى التأكد من وجوده بجانب ملف التشغيل.")
    st.stop()

profile = DEVICE_PROFILES[st.session_state.device_mode]
min_h = profile["height"]

cache_buster = f"<!-- nonce: {st.session_state.reload_nonce} -->"
auto_resize_script = f"""
<script>
(function() {{
  function syncHeight() {{
    try {{
      const frame = window.frameElement;
      if (!frame) return;
      const doc = document.documentElement;
      const body = document.body;
      const contentHeight = Math.max(
        body ? body.scrollHeight : 0,
        doc ? doc.scrollHeight : 0,
        {min_h}
      );
      frame.style.height = (contentHeight + 36) + "px";
    }} catch (e) {{}}
  }}
  window.addEventListener("load", () => {{
    syncHeight();
    setTimeout(syncHeight, 250);
    setTimeout(syncHeight, 800);
  }});
  window.addEventListener("click", () => {{
    setTimeout(syncHeight, 120);
    setTimeout(syncHeight, 450);
  }});
  if (typeof ResizeObserver !== "undefined") {{
    const ro = new ResizeObserver(syncHeight);
    ro.observe(document.documentElement);
  }}
}})();
</script>
"""

if "</body>" in html_content:
    embedded_html = html_content.replace("</body>", f"{auto_resize_script}\n{cache_buster}\n</body>")
else:
    embedded_html = html_content + "\n" + auto_resize_script + "\n" + cache_buster

st.markdown(
    f"""
    <div class="astro-frame-outer">
      <div class="astro-frame-wrap" style="width: {profile['width']}; max-width: 100%;">
    """,
    unsafe_allow_html=True,
)

components.html(
    embedded_html,
    height=profile["height"],
    scrolling=True,
)

st.markdown(
    """
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
