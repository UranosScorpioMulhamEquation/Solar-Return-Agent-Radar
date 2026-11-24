import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="اسأل استرو رادار | عرض شاشة كاملة",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HTML_FILENAME = "Full_ask_astro_radar.html"


def load_html_file(filename: str) -> tuple[str | None, str]:
    """يبحث عن ملف HTML في مجلد التطبيق الحالي أو المجلدات المجاورة ويعيد محتواه."""
    base_dir = Path(__file__).resolve().parent
    candidate_paths = [
        base_dir / filename,
        Path.cwd() / filename,
        base_dir / "assets" / filename,
        base_dir / "static" / filename,
    ]
    for path in candidate_paths:
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8"), str(path)

    # بحث احتياطي في المجلدات الفرعية القريبة
    for match in base_dir.rglob(filename):
        if match.is_file():
            return match.read_text(encoding="utf-8"), str(match)

    return None, str(candidate_paths[0])


html_content, resolved_path = load_html_file(HTML_FILENAME)

if "cinema_mode" not in st.session_state:
    st.session_state.cinema_mode = True

if "viewer_height" not in st.session_state:
    st.session_state.viewer_height = 1150

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

      .stApp {
        background: radial-gradient(circle at 15% 10%, #121c33 0%, #07090e 58%, #05070b 100%);
        color: #f8fafc;
      }

      /* إزالة الحشوات الزائدة لجعله أقرب لملء الشاشة */
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

      /* شريط علوي أنيق للواجهة الرسومية */
      .radar-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        background: linear-gradient(135deg, rgba(14, 19, 34, 0.95), rgba(19, 31, 54, 0.92));
        border: 1px solid rgba(253, 230, 138, 0.24);
        border-radius: 14px;
        padding: 10px 16px;
        margin-bottom: 10px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
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
        letter-spacing: 0.2px;
      }

      .radar-sub {
        margin: 0;
        font-size: 0.8rem;
        color: #94a3b8;
      }

      .radar-badge {
        background: rgba(2, 132, 199, 0.18);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #bae6fd;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
      }

      /* أزرار التدرج الأزرق */
      div.stButton > button, div.stDownloadButton > button {
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

      div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-1px);
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        border-color: #fde68a !important;
      }

      /* إطار عرض صفحة HTML */
      .astro-frame-wrap {
        background: #0e1322;
        border: 1px solid rgba(253, 230, 138, 0.22);
        border-radius: 16px;
        padding: 6px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.6);
      }

      iframe {
        border-radius: 12px !important;
        background: #edf1ee;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# الشريط العلوي للواجهة
st.markdown(
    f"""
    <div class="radar-topbar">
      <div class="radar-brand">
        <span class="radar-dot"></span>
        <div>
          <p class="radar-title">اسأل استرو رادار — عارض الشاشة الكاملة</p>
          <p class="radar-sub">عرض مباشر ومستقل لملف {HTML_FILENAME}</p>
        </div>
      </div>
      <span class="radar-badge">وضع العرض الكامل نشط</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# شريط أدوات خفيف ومباشر
col_a, col_b, col_c, col_d = st.columns([1.3, 1.3, 1.4, 2.0])

with col_a:
    if st.button("🔄 تحديث العرض", use_container_width=True):
        st.session_state.reload_nonce += 1
        st.rerun()

with col_b:
    height_choice = st.selectbox(
        "ارتفاع الإطار",
        options=[950, 1150, 1450, 1800],
        index=[950, 1150, 1450, 1800].index(st.session_state.viewer_height)
        if st.session_state.viewer_height in [950, 1150, 1450, 1800]
        else 1,
        label_visibility="collapsed",
    )
    st.session_state.viewer_height = height_choice

with col_c:
    if html_content:
        st.download_button(
            label="⬇️ تحميل HTML",
            data=html_content.encode("utf-8"),
            file_name=HTML_FILENAME,
            mime="text/html",
            use_container_width=True,
        )

with col_d:
    if html_content:
        st.caption(f"المصدر: `{Path(resolved_path).name}` ({len(html_content):,} حرف)")

if html_content is None:
    st.error(
        f"لم يتم العثور على الملف `{HTML_FILENAME}` بجانب `app.py` في مجلد المشروع. "
        "يرجى رفع الملفين معاً في نفس المجلد أو مستودع GitHub."
    )
    st.stop()

# تضمين الملف المرفق مع ضبط تلقائي لارتفاع الإطار حسب محتوى الصفحة الداخلية
# وإضافة مفتاح ديناميكي (reload_nonce) لإعادة التحميل عند الطلب
cache_buster = f"<!-- nonce: {st.session_state.reload_nonce} -->"
auto_resize_script = """
<script>
(function() {
  function syncHeight() {
    try {
      const frame = window.frameElement;
      if (!frame) return;
      const doc = document.documentElement;
      const body = document.body;
      const contentHeight = Math.max(
        body ? body.scrollHeight : 0,
        doc ? doc.scrollHeight : 0,
        """ + str(st.session_state.viewer_height) + """
      );
      frame.style.height = (contentHeight + 36) + "px";
    } catch (e) {}
  }
  window.addEventListener("load", () => {
    syncHeight();
    setTimeout(syncHeight, 250);
    setTimeout(syncHeight, 800);
  });
  window.addEventListener("click", () => {
    setTimeout(syncHeight, 120);
    setTimeout(syncHeight, 450);
  });
  if (typeof ResizeObserver !== "undefined") {
    const ro = new ResizeObserver(syncHeight);
    ro.observe(document.documentElement);
  }
})();
</script>
"""

if "</body>" in html_content:
    embedded_html = html_content.replace("</body>", f"{auto_resize_script}\n{cache_buster}\n</body>")
else:
    embedded_html = html_content + "\n" + auto_resize_script + "\n" + cache_buster

st.markdown('<div class="astro-frame-wrap">', unsafe_allow_html=True)
components.html(
    embedded_html,
    height=st.session_state.viewer_height,
    scrolling=True,
)
st.markdown("</div>", unsafe_allow_html=True)
