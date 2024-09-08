import streamlit as st
from PIL import Image
from db import init_db, register_user, login_user
from prompt_generators import (
    generate_prompt_co_star,
    generate_prompt_crispe,
    generate_prompt_icio,
    generate_prompt_broke,
    generate_prompt_midjourney,
    modify_output
)
from helpers import calculate_height

# 初始化数据库
init_db()

# 定义框架及其介绍
framework_descriptions = {
    "CO-STAR": "适用于背景丰富、需要多维度定制输出的场景，如专业报告、市场分析。",
    "CRISPE": "适用于角色扮演和模拟的场景，如个性化互动、情境模拟。",
    "ICIO": "适用于明确任务指令和格式的场景，如数据处理、内容创作、技术任务。",
    "BROKE": "适用于项目管理和持续改进的场景，如创意设计、研究分析。",
    "Midjourney": "生成高质量的绘画提示词，将用户输入的画面描述拆解为镜头、光线、主体、背景、风格和氛围六个要素，进行补充和完善。"
}

def main():
    # 用户认证相关逻辑
    username_input = st.sidebar.text_input("用户名")
    password_input = st.sidebar.text_input("密码", type="password")

    if st.sidebar.button("登录"):
        if login_user(username_input, password_input):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username_input
            st.sidebar.success(f"欢迎回来, {username_input}!")
        else:
            st.sidebar.error("登录失败，请检查用户名或密码。")

    if st.sidebar.button("注册"):
        if username_input and password_input:
            register_user(username_input, password_input)
        else:
            st.sidebar.error("请填写完整的用户名和密码进行注册。")

    # 主功能界面
    st.title("多框架提示词助手")
    col1, col2, col3, col4, col5 = st.columns(5)

    # 框架选择
    if 'framework' not in st.session_state:
        st.session_state['framework'] = None

    with col1:
        if st.button("CO-STAR"):
            st.session_state['framework'] = "CO-STAR"
    with col2:
        if st.button("CRISPE"):
            st.session_state['framework'] = "CRISPE"
    with col3:
        if st.button("ICIO"):
            st.session_state['framework'] = "ICIO"
    with col4:
        if st.button("BROKE"):
            st.session_state['framework'] = "BROKE"
    with col5:
        if st.button("Midjourney"):
            st.session_state['framework'] = "Midjourney"

    if st.session_state['framework']:
        selected_framework = st.session_state['framework']
        st.write(f"你选择了: {selected_framework}")
        st.write(framework_descriptions[selected_framework])

    user_input = st.text_input("请输入您的任务", placeholder="例如：写一篇宣传AI的小红书")

    # 生成提示词逻辑
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if st.button("生成提示词"):
            if user_input:
                framework = st.session_state['framework']
                output = generate_prompt(user_input, framework)
                st.session_state['initial_output'] = output

        if 'initial_output' in st.session_state:
            st.write(f"初始 {st.session_state['framework']} 提示词:")
            st.text_area("初始提示词", value=st.session_state['initial_output'],
                         height=calculate_height(st.session_state['initial_output']), key="initial_text")

        modification_input = st.text_input("提出需要修改的点", placeholder="例如：请更加注重营销角度")

        if st.button("修改提示词"):
            if modification_input:
                modified_output = modify_output(modification_input, st.session_state['initial_output'], st.session_state['framework'])
                st.session_state['modified_output'] = modified_output

            if 'modified_output' in st.session_state:
                st.write(f"修改后的 {st.session_state['framework']} 提示词:")
                st.text_area("修改后的提示词", value=st.session_state['modified_output'],
                             height=calculate_height(st.session_state['modified_output']), key="modified_text")
    else:
        st.info("请先登录以使用功能。")
        st.button("生成提示词", disabled=True)
        st.text_input("提出需要修改的点", disabled=True)

if __name__ == "__main__":
    main()
