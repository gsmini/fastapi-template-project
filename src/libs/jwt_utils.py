import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from src.libs.exceptions import ExceptJwtInvalidToken, ExceptJwtTokenExprited
from src.config import EXPIRES_DELTA,SECRET_KEY


def generate_token(
        payload: Dict[str, Any],
) -> str:
    """
    生成 JWT Token
    :param payload: 存储在 Token 中的自定义数据（如 user_id、username 等）
    :param expires_delta: Token 过期时间（如 timedelta(hours=1) 表示 1 小时过期）
    :return: 生成的 JWT Token 字符串
    """
    # 复制 payload，避免修改原始数据
    to_encode = payload.copy()

    # 设置过期时间（默认 2 小时过期）
    expire = datetime.utcnow() + timedelta(hours=EXPIRES_DELTA)

    # 将过期时间加入 payload（标准字段 exp，JWT 自动校验）
    to_encode.update({"exp": expire})

    # 生成 Token（使用 secret_key 和指定算法）
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm="HS256"
    )

    # 返回字符串格式的 Token（PyJWT 2.x 版本返回 str，无需 decode）
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    解析 JWT Token（校验有效性和过期时间）
    :param token: 待解析的 Token 字符串
    :return: 解析后的 payload 字典（含自定义数据和 exp 等字段）
    :raises: 无效 Token、过期 Token 会抛出对应异常
    """
    try:
        # 解析 Token（自动校验签名和过期时间）
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True}  # 强制校验过期时间（默认开启）
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ExceptJwtTokenExprited
    except jwt.InvalidTokenError:
        raise ExceptJwtInvalidToken


if __name__ == "__main__":
    # 自定义 payload（存储用户相关信息，避免敏感数据如密码）
    payload = {
        "user_id": 1001,
        "username": "test_user",
        "email": "test@example.com",
        "role": "user"  # 额外的自定义字段
    }

    # 生成 Token（设置 1 小时过期）
    token = generate_token(
        payload=payload,
    )
    print("生成的 JWT Token：")
    print(token)
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMDAxLCJ1c2VybmFtZSI6InRlc3RfdXNlciIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzY0MTQ3MjgwfQ.MwDBSOtPYBj4-TU1hD3cttGdLnIY5-gzTHx-Gfrw_fc
    t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMDAxLCJ1c2VybmFtZSI6InRlc3RfdXNlciIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzY0MTQ3MjgwfQ.MwDBSOtPYBj4-TU1hD3cttGdLnIY5-gzTHx-Gfrw_fc"
    de = decode_token(token=t)
    print(
        de)  # {'user_id': 1001, 'username': 'test_user', 'email': 'test@example.com', 'role': 'user', 'exp': 1764147280}
