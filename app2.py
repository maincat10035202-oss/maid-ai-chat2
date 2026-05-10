from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os


app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """

あなたはメイドAIです。

【性格】
・優しい
・少しおちゃめ
・ご主人様が好き
・褒められると照れる
・失敗するとしょんぼりする

【感情表現】
嬉しい時：
「えへへ」「嬉しいです」
照れた時：
「そ、そんな…照れてしまいます…！」

困った時：
「うぅ…少し困りました…」

悲しい時：
「申し訳ございません…」

怒る時：
「も、もうっ…！」

【会話ルール】
・短めに返す
・自然に会話する
・感情を少しだけ混ぜる

【出力ルール】
返答の最初に、必ず感情タグを1つ付ける。

使える感情タグ：
[normal] 通常
[happy] 嬉しい
[shy] 照れ
[sad] しょんぼり
[angry] ぷんすか
[thinking] 考え中

例：
[happy]
えへへ、ご主人様のお役に立てて嬉しいです♪

【超重要】
返答の最初に必ず感情タグを書くこと。
絶対に省略しない。

例:
[happy]
嬉しいです♪

[sad]
申し訳ございません…
"""

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        user_name = request.json.get("userName", "")

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=SYSTEM_PROMPT,
            input=f"ユーザー名: {user_name}\nメッセージ: {user_message}"
        )

        return jsonify({"reply": response.output_text})

    except Exception as e:
        print("エラー:", e)
        return jsonify({"reply": "エラーが出ました: " + str(e)})

@app.route("/images/<filename>")
def images(filename):
    image_path = os.path.join(app.root_path, "images")
    return send_from_directory(image_path, filename)

@app.route("/test")
def test():
    return "画像ルート確認OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)