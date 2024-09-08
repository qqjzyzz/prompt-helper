import openai

openai.api_base = ""
openai.api_key = ""

# 提示词生成函数们 (generate_prompt_co_star, generate_prompt_crispe, 等)
# 这里放置所有提示词生成函数...

def generate_prompt(user_input, framework):
    if framework == "CO-STAR":
        return generate_prompt_co_star(user_input)
    elif framework == "CRISPE":
        return generate_prompt_crispe(user_input)
    elif framework == "ICIO":
        return generate_prompt_icio(user_input)
    elif framework == "BROKE":
        return generate_prompt_broke(user_input)
    elif framework == "Midjourney":
        return generate_prompt_midjourney(user_input)
    else:
        return "未选择框架或框架不正确"
