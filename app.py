import streamlit as st
from PIL import Image, ImageOps
import base64
import io
import os
import time
from datetime import datetime, timedelta, timezone


# NUS配色
NUS_BLUE = "#00205B"
NUS_ORANGE = "#FF6F0F"
NUS_DARK_BLUE = "#17408B"
NUS_WHITE = "#f7f9fb"

# 默认头像
DEFAULT_USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
def get_base64_of_local_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return "data:image/png;base64," + base64.b64encode(data).decode()

desktop_path = os.path.expanduser("~/Desktop/chatbot_image.png")

DEFAULT_BOT_AVATAR = get_base64_of_local_image(desktop_path)

#DEFAULT_BOT_AVATAR = get_base64_of_local_image("/Users/lankun/Desktop/chatbot_image.png")

def save_avatar(email, avatar_b64):
    if email:
        with open(f"profile_{email}.txt", "w") as f:
            f.write(avatar_b64)

def load_avatar(email):
    try:
        with open(f"profile_{email}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return DEFAULT_USER_AVATAR

def pad_to_square(img: Image.Image, color=(247, 249, 251)):
    x, y = img.size
    size = max(x, y)
    new_img = Image.new('RGB', (size, size), color)
    new_img.paste(img, ((size - x) // 2, (size - y) // 2))
    return new_img

def show_profile_modal():
    st.markdown(
        "<div style='display:flex;align-items:center;'>"
        "<span style='font-size:22px;font-weight:bold;margin-left:8px;'>设置 / Settings</span>"
        "</div>",
        unsafe_allow_html=True
    )
    email = st.text_input("邮箱 / Email", value=st.session_state.profile["email"])
    uploaded_avatar = st.file_uploader("上传头像 / Upload Avatar", type=["png", "jpg", "jpeg"])
    if uploaded_avatar:
        image = Image.open(uploaded_avatar)
        image = pad_to_square(image)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        avatar_b64 = "data:image/png;base64," + base64.b64encode(byte_im).decode()
        st.session_state.profile["avatar"] = avatar_b64
    if st.button("保存 / Save"):
        st.session_state.profile["email"] = email
        save_avatar(email, st.session_state.profile["avatar"])
        st.success("已保存 / Saved!")
    st.image(st.session_state.profile["avatar"], width=80, caption="当前头像 / Current Avatar")

LANGUAGES = {
    "中文": {
        "welcome": "欢迎来到 GenAI 租户助手",
        "choose_login": "请选择登录方式：",
        "email_login": "邮箱登录",
        "login": "登录",
        "skip": "跳过",
        "menu": ["对话", "合同问答", "报修", "租金提醒"],
        "chat_title": "租户对话",
        "chat_placeholder": "请输入您的问题...",
        "chat_reply": "应用仍在开发中，感谢您的体验！",
        "contract_title": "合同条款智能问答",
        "contract_upload": "上传租赁合同PDF",
        "contract_question": "请输入您的问题",
        "contract_info": "应用仍在开发中，暂不支持合同问答。",
        "repair_title": "报修申请",
        "repair_desc": "请描述您的报修问题",
        "repair_img": "上传图片（可选）",
        "repair_submit": "提交报修",
        "repair_success": "报修已提交！（模拟）",
        "rent_title": "租金提醒",
        "rent_info": "应用仍在开发中，暂不支持租金数据。",
        "lang_select": "选择语言"
    },
    "English": {
        "welcome": "Welcome to GenAI Tenant Assistant",
        "choose_login": "Please choose a login method:",
        "email_login": "Email Login",
        "login": "Login",
        "skip": "Skip",
        "menu": ["Chat", "Contract Q&A", "Repair", "Rent Reminder"],
        "chat_title": "Tenant Chat",
        "chat_placeholder": "Type your question...",
        "chat_reply": "The app is still under development. Thank you for trying!",
        "contract_title": "Contract Q&A",
        "contract_upload": "Upload Rental Contract PDF",
        "contract_question": "Enter your question",
        "contract_info": "Feature under development, contract Q&A not supported yet.",
        "repair_title": "Repair Request",
        "repair_desc": "Describe your repair issue",
        "repair_img": "Upload image (optional)",
        "repair_submit": "Submit Repair",
        "repair_success": "Repair submitted! (Mock)",
        "rent_title": "Rent Reminder",
        "rent_info": "Feature under development, rent data not supported yet.",
        "lang_select": "Select Language"
    },
    "Melayu": {
        "welcome": "Selamat datang ke Pembantu Penyewa GenAI",
        "choose_login": "Sila pilih kaedah log masuk:",
        "email_login": "Log Masuk Emel",
        "login": "Log Masuk",
        "skip": "Langkau",
        "menu": ["Sembang", "Soal Jawab Kontrak", "Pembaikan", "Peringatan Sewa"],
        "chat_title": "Sembang Penyewa",
        "chat_placeholder": "Sila taip soalan anda...",
        "chat_reply": "Aplikasi masih dalam pembangunan. Terima kasih kerana mencuba!",
        "contract_title": "Soal Jawab Kontrak",
        "contract_upload": "Muat naik PDF Kontrak Sewa",
        "contract_question": "Masukkan soalan anda",
        "contract_info": "Ciri masih dalam pembangunan, Soal Jawab Kontrak belum disokong.",
        "repair_title": "Permohonan Pembaikan",
        "repair_desc": "Sila huraikan isu pembaikan anda",
        "repair_img": "Muat naik gambar (pilihan)",
        "repair_submit": "Hantar Pembaikan",
        "repair_success": "Pembaikan dihantar! (Mock)",
        "rent_title": "Peringatan Sewa",
        "rent_info": "Ciri masih dalam pembangunan, data sewa belum disokong.",
        "lang_select": "Pilih Bahasa"
    },
    "தமிழ்": {
        "welcome": "GenAI வாடிக்கையாளர் உதவிக்கு வரவேற்கிறோம்",
        "choose_login": "உள்நுழைவு முறையைத் தேர்ந்தெடுக்கவும்:",
        "email_login": "மின்னஞ்சல் உள்நுழைவு",
        "login": "உள்நுழை",
        "skip": "தவிர்",
        "menu": ["உரையாடல்", "ஒப்பந்த கேள்வி/பதில்", "பழுது", "வாடகை நினைவூட்டல்"],
        "chat_title": "வாடிக்கையாளர் உரையாடல்",
        "chat_placeholder": "உங்கள் கேள்வியை உள்ளிடவும்...",
        "chat_reply": "பயன்பாடு இன்னும் உருவாக்கத்தில் உள்ளது. முயற்சித்ததற்கு நன்றி!",
        "contract_title": "ஒப்பந்த கேள்வி/பதில்",
        "contract_upload": "வாடகை ஒப்பந்த PDF பதிவேற்றவும்",
        "contract_question": "உங்கள் கேள்வியை உள்ளிடவும்",
        "contract_info": "இது இன்னும் உருவாக்கத்தில் உள்ளது, ஒப்பந்த கேள்வி/பதில் ஆதரிக்கப்படவில்லை.",
        "repair_title": "பழுது விண்ணப்பம்",
        "repair_desc": "உங்கள் பழுது பிரச்சினையை விவரிக்கவும்",
        "repair_img": "படத்தை பதிவேற்றவும் (விருப்பத்தேர்வு)",
        "repair_submit": "பழுது சமர்ப்பிக்கவும்",
        "repair_success": "பழுது சமர்ப்பிக்கப்பட்டது! (Mock)",
        "rent_title": "வாடகை நினைவூட்டல்",
        "rent_info": "இது இன்னும் உருவாக்கத்தில் உள்ளது, வாடகை தரவுகள் ஆதரிக்கப்படவில்லை.",
        "lang_select": "மொழியைத் தேர்ந்தெடுக்கவும்"
    }
}

# 侧边栏和主色调样式
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #f7f9fb 0%, #e6f0fa 100%);
        min-height: 100vh;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background: linear-gradient(135deg, {NUS_BLUE} 60%, #3a5ba0 100%);
        min-height: 100vh;
    }}
    .stSelectbox > div {{
        background: {NUS_ORANGE};
        border-radius: 8px;
        color: #111 !important;
        font-weight: bold;
        box-shadow: 0 2px 8px #ff6f0f22;
    }}
    .stRadio > div {{
        background: {NUS_BLUE};
        border-radius: 12px;
        padding: 8px 0;
        color: #fff !important;
        font-weight: bold;
        box-shadow: 0 2px 8px #00205b33;
    }}
    .stRadio label, .stRadio span {{
        color: #fff !important;
        font-weight: bold !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 2px #00205b, 0 0 2px #fff;
        letter-spacing: 1px;
    }}
    .css-1v0mbdj, .css-1d391kg {{
        background: {NUS_BLUE} !important;
    }}
    .sidebar-content, .stSidebarContent {{
        background: {NUS_BLUE} !important;
    }}
    .bubble-user {{
        box-shadow: 0 2px 8px #ff6f0f33;
        border: 1.5px solid #ff6f0f44;
    }}
    .bubble-bot {{
        box-shadow: 0 2px 8px #00205b33;
        border: 1.5px solid #00205b44;
    }}
    .art-title {{
        font-family: 'Segoe UI', 'Arial Black', 'Arial', sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        color: {NUS_ORANGE};
        letter-spacing: 2px;
        text-shadow: 2px 2px 8px #00205b44, 0 2px 8px #fff;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .art-title .icon {{
        font-size: 2.2rem;
        margin-right: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 新加坡时区
SGT = timezone(timedelta(hours=8))

# 加载动图（你可以换成自己的gif）
LOADING_GIF = "https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif"

# 选择语言
if "lang" not in st.session_state:
    st.session_state.lang = "中文"
L = LANGUAGES[st.session_state.lang]

st.sidebar.markdown(
    f"<div style='color:{NUS_ORANGE};font-weight:bold;font-size:18px;margin-bottom:8px'>{L['lang_select']}</div>",
    unsafe_allow_html=True
)
st.sidebar.selectbox(
    "",
    list(LANGUAGES.keys()),
    index=list(LANGUAGES.keys()).index(st.session_state.lang),
    key="lang",
    on_change=lambda: st.session_state.update(lang=st.session_state.lang)
)
L = LANGUAGES[st.session_state.lang]

if "profile" not in st.session_state:
    st.session_state.profile = {
        "email": "",
        "avatar": DEFAULT_USER_AVATAR
    }


# 页面切换控制
if "page" not in st.session_state:
    st.session_state.page = "login"

# 登录/跳过后，加载头像
if st.session_state.page == "main" and st.session_state.profile["email"]:
    st.session_state.profile["avatar"] = load_avatar(st.session_state.profile["email"])

# ----------- 初始化会话状态，防止KeyError -----------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "loading" not in st.session_state:
    st.session_state["loading"] = False


# ----------- 页面渲染 -----------
if st.session_state.page == "login":
    st.markdown(f"<h1 style='text-align:center;margin-top:120px;color:{NUS_BLUE}'>{L['welcome']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:{NUS_BLUE}'>{L['choose_login']}</p>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stButton > button {
        width: 120px;
        height: 46px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 14px;
        border: none;
        background: linear-gradient(145deg, #fff 60%, #e6f0fa 100%);
        margin: 0 16px 0 0;
        box-shadow: 0 6px 18px #00205b22, 0 1.5px 0 #fff inset, 0 -2px 8px #ff6f0f11 inset;
        transition: background 0.15s, box-shadow 0.15s, border 0.15s, transform 0.1s;
        outline: none;
        color: #00205B;
        letter-spacing: 1px;
        position: relative;
    }
    .stButton > button::after {
        content: "";
        position: absolute;
        left: -5px; top: -5px; right: -5px; bottom: -5px;
        border-radius: 18px;
        border: 2.5px solid #ff6f0f;
        pointer-events: none;
        transition: border-color 0.15s, box-shadow 0.15s;
        box-shadow: 0 0 0 0 #ff6f0f00;
    }
    .stButton > button:hover::after {
        border-color: #ff6f0f;
        box-shadow: 0 0 0 4px #ff6f0f22;
    }
    .stButton > button:active::after {
        border-color: #d35400;
        box-shadow: 0 0 0 2px #ff6f0f55;
    }
    .stButton > button:active {
        background: linear-gradient(135deg, #ffe5cc 60%, #ffd6b3 100%);
        transform: translateY(2.5px) scale(0.97);
    }
    </style>
    """, unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input(L["email_login"])
        col_btn1, col_btn2 = st.columns([1,1])
        with col_btn1:
            login_clicked = st.form_submit_button(L["login"])
        with col_btn2:
            skip_clicked = st.form_submit_button(L["skip"])
        if login_clicked:
            st.session_state.page = "main"
            st.session_state.profile["email"] = email
            st.stop()
        if skip_clicked:
            st.session_state.page = "main"
            st.stop()
    st.stop()
    st.stop()

# ----------- 主页面 -----------
elif st.session_state.page == "main":
    colA, colB = st.columns([10,1])
    with colB:
        if st.button("⚙️", key="profile_btn"):
            st.session_state.page = "settings"
            st.rerun()

    menu = st.sidebar.radio(
        "Menu",
        L["menu"],
        index=0,
        key="menu_radio",
        label_visibility="collapsed"
    )

    if menu == L["menu"][0]:  # 对话/Chat
        st.markdown(
            f"""
            <div class='art-title'><span class='icon'>💬</span>{L['chat_title']}</div>
            """,
            unsafe_allow_html=True
        )

        for idx, (role, msg, ts) in enumerate(st.session_state["chat_history"]):
            if role == "user":
                st.markdown(
                    f"""
                    <div style='display:flex;justify-content:flex-end;align-items:flex-start;'>
                        <div class='bubble-user' style='background:{NUS_ORANGE};color:#111;padding:10px 18px;border-radius:16px 4px 16px 16px;margin:8px 0;max-width:60%;font-size:16px;font-weight:bold;order:2;'>
                            {msg}
                            <div style='font-size:12px;font-weight:400;color:#888;margin-top:4px;text-align:right;'>{ts}</div>
                        </div>
                        <div style='margin-left:8px;order:3;display:flex;align-items:flex-end;position:relative;top:-18px;'>
                            <img src="{st.session_state.profile['avatar']}" width="40" height="40" style="border-radius:50%;border:2px solid {NUS_ORANGE};object-fit:cover;background:#fff"/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='display:flex;justify-content:flex-start;align-items:flex-start;'>
                        <div style='margin-right:8px;order:1;display:flex;align-items:flex-end;position:relative;top:-18px;'>
                            <img src="{DEFAULT_BOT_AVATAR}" width="40" height="40" style="border-radius:50%;border:2px solid {NUS_BLUE};object-fit:cover;background:#fff"/>
                        </div>
                        <div class='bubble-bot' style='background:{NUS_DARK_BLUE};color:#111;padding:10px 18px;border-radius:4px 16px 16px 16px;margin:8px 0;max-width:60%;font-size:16px;font-weight:bold;order:2;'>
                            {msg}
                            <div style='font-size:12px;font-weight:400;color:#888;margin-top:4px;text-align:left;'>{ts}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
            # 加载动图
            if st.session_state["loading"] and idx == len(st.session_state["chat_history"]) - 1 and role == "user":
                st.markdown(
                    f"""
                    <div style='display:flex;justify-content:flex-start;align-items:center;'>
                      <div style='margin-right:8px;order:1;display:flex;align-items:center;'>
                        <img src="{DEFAULT_BOT_AVATAR}" width="40" height="40" style="border-radius:50%;border:2px solid {NUS_BLUE};object-fit:cover;background:#fff"/>
                      </div>
                      <div style='background:#fff;padding:6px 12px;border-radius:12px;max-width:60%;display:flex;align-items:center;'>
                        <img src="{LOADING_GIF}" width="28" height="28" style="vertical-align:middle;"/>
                        <span style='margin-left:8px;color:#888;font-size:14px;'>思考中...</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True
                )

        # 多语言“输入不能为空”提示
        EMPTY_INPUT_MSG = {
            "中文": "输入信息不能为空",
            "English": "Input cannot be empty",
            "Melayu": "Input tidak boleh kosong",
            "தமிழ்": "உள்ளீடு காலியாக இருக்க முடியாது"
        }
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(L["chat_placeholder"], key="chat_input")
            submitted = st.form_submit_button("发送" if st.session_state.lang=="中文" else "Send")
            if submitted:
                if not user_input.strip():
                    st.markdown(f"<div style='color:#d9534f;font-size:13px;margin-top:-8px;margin-bottom:4px'>⚠️ {EMPTY_INPUT_MSG.get(st.session_state.lang, '输入信息不能为空')}</div>", unsafe_allow_html=True)
                else:
                    now = datetime.now(SGT).strftime("%Y/%m/%d %H:%M:%S")
                    st.session_state["chat_history"].append(("user", user_input, now))
                    st.session_state["loading"] = True
                    st.rerun()

        # 机器人回复模拟（带延迟和时间戳）
        if st.session_state["loading"]:
            time.sleep(1.2)
            now = datetime.now(SGT).strftime("%Y/%m/%d %H:%M:%S")
            st.session_state["chat_history"].append(("bot", L["chat_reply"], now))
            st.session_state["loading"] = False
            st.rerun()

    elif menu == L["menu"][1]:  # 合同问答/Contract Q&A
        st.markdown(f"<h2 style='color:{NUS_ORANGE};font-weight:bold'>{L['contract_title']}</h2>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(L["contract_upload"], type="pdf")
        with st.form("contract_qa_form"):
            question = st.text_input(L["contract_question"])
            send_clicked = st.form_submit_button("发送" if st.session_state.lang=="中文" else "Send")
        if uploaded_file and question and send_clicked:
            st.info(L["contract_info"])

    elif menu == L["menu"][2]:  # 报修/Repair
        st.markdown(f"<h2 style='color:{NUS_ORANGE};font-weight:bold'>{L['repair_title']}</h2>", unsafe_allow_html=True)
        with st.form("repair_form"):
            desc = st.text_area(L["repair_desc"])
            img = st.file_uploader(L["repair_img"], type=["jpg", "png", "jpeg"])
            send_clicked = st.form_submit_button("发送" if st.session_state.lang=="中文" else "Send")
            if send_clicked:
                st.success(L["repair_success"])

    elif menu == L["menu"][3]:  # 租金提醒/Rent Reminder
        st.markdown(f"<h2 style='color:{NUS_ORANGE};font-weight:bold'>{L['rent_title']}</h2>", unsafe_allow_html=True)
        st.info(L["rent_info"])

# ----------- 设置页面 -----------
elif st.session_state.page == "settings":
    if st.button("⬅️ 返回", key="back_btn"):
        st.session_state.page = "main"
        st.rerun()
    show_profile_modal()
    st.stop()
