import requests

# --- 你的 Authing 应用配置 ---
AUTHING_APP_ID = "6a0099b774fc964d8b9f9988"
AUTHING_APP_SECRET = "5a184ba556296c78969fc7963722f69d"
AUTHING_API_BASE = "https://brgxbqrxoz7r-demo.authing.cn"          # 修正后的根地址
AUTHING_OIDC_URL = "https://brgxbqrxoz7r-demo.authing.cn/oidc"     # OIDC 端点专用

def send_sms_code(phone):
    """第一步：给指定手机号发送验证码"""
    url = f"{AUTHING_API_BASE}/api/v2/sms/send"     # 用根地址，不再是 /oidc/
    payload = {
        "phone": phone,
        "channel": "login",
        "appId": AUTHING_APP_ID
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get("code") == 200:
            return True, "验证码已发送，请查收短信"
        else:
            return False, f"发送失败：{data.get('message', '未知错误')}"
    except Exception as e:
        return False, f"请求失败：{e}"

def verify_sms_code(phone, code):
    """第二步：用手机号和验证码换取用户令牌"""
    url = f"{AUTHING_OIDC_URL}/token"               # token 端点仍走 /oidc/
    payload = {
        "grant_type": "password",
        "client_id": AUTHING_APP_ID,
        "client_secret": AUTHING_APP_SECRET,
        "username": phone,
        "password": code,
        "scope": "openid profile phone"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200 and "access_token" in data:
            return True, data["access_token"], data.get("id_token", "")
        else:
            return False, None, f"验证失败：{data.get('error_description', '请检查验证码是否正确')}"
    except Exception as e:
        return False, None, f"请求失败：{e}"

def get_user_info(access_token):
    """第三步：用令牌获取用户信息"""
    url = f"{AUTHING_OIDC_URL}/me"                  # 用户信息也走 /oidc/
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return True, data
        else:
            return False, f"获取用户信息失败：{data.get('message', '未知错误')}"
    except Exception as e:
        return False, f"请求失败：{e}"