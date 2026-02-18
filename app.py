import streamlit as st
from openai import OpenAI

# ==========================================
# 1. 核心配置
# ==========================================
# 从云端保险箱读取密钥
API_KEY = st.secrets["DEEPSEEK_API_KEY"] 
BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

st.set_page_config(page_title="外贸嘴替 Pro", page_icon="🌍", layout="centered")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

# ==========================================
# 2. 商业闭环 (收钱的逻辑在这里！)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/wechat.png", width=50) # 微信图标
    st.markdown("### 🔓 解锁完整版")
    st.markdown("扫码或加V：**liao13689209126**") # ★★★ 改成你的微信号
    st.markdown("获取专属访问密码，仅需 9.9元/月")
    
    # 密码输入框
    secret_pass = st.text_input("请输入访问密码", type="password")
    
    st.info("💡 为什么要收费？\n因为集成了昂贵的 DeepSeek-V3 商业版模型，确保生成的商务邮件最地道。")

# ==========================================
# 3. 逻辑判断
# ==========================================
# 只有密码对，或者没输密码时给个预览，才能往下走
# 这里我们设置密码为 "8888" (你可以自己改)
if secret_pass != "3361":
    st.title("🌍 外贸嘴替 Pro")
    st.warning("🔒 请在左侧输入密码解锁使用。")
    st.markdown("#### 它可以帮你：")
    st.markdown("- ✅ 委婉安抚客户")
    st.markdown("- ✅ 专业商务沟通")
    st.markdown("- ✅ 强硬催款维权")
    st.stop() # 停止运行下面的代码

# ==========================================
# 4. 只有解锁后才会显示的主程序
# ==========================================
tone = st.selectbox(
    "请选择回复语气：",
    ("🤝 委婉客气 (适合安抚客户)", "💼 专业商务 (适合日常沟通)", "🔥 强硬严肃 (适合催款/维权)")
)

SYSTEM_PROMPT = f"""
你是一位拥有 20 年经验的资深外贸总监，精通欧美商务文化。
用户的当前意图是：{tone}。

【任务要求】
1. 将用户的中文意图，转化为地道、得体、高情商的【英文邮件】。
2. 格式：
   Subject: [自动生成吸引人的标题]
   Dear [Name],
   [正文]
   Best regards,
   [Your Name]
3. 附带中文解析：在邮件下方，用中文解释为什么这么写（比如：这里用了虚拟语气表示委婉）。
"""

def polish_text(user_text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=1.3,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 出错: {str(e)}"

st.title("🌍 外贸嘴替 Pro (已解锁)")
user_input = st.text_area("请输入素材：", height=150, placeholder="例：客户嫌运费贵，我想解释是因为我们要走空运，速度快...")

if st.button("🚀 立即润色", type="primary"):
    if not user_input:
        st.warning("请先输入内容！")
    else:
        with st.spinner("AI 正在奋笔疾书..."):
            result = polish_text(user_input)
            st.markdown(result)
            st.success("生成的真不错！")