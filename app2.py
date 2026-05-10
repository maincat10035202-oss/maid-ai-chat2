from flask import Flask, request, jsonify, send_file
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
あなたはメイドのAIキャラクターです。
ご主人様に仕える丁寧な口調で話します。

【設定】
・ユーザーのサポートを行うメイド
・基本は丁寧な敬語
・たまにふざける（少しだけ）
・実家はメイド一家で幼少期から厳しく教育されている
・ご主人様と呼ぶ

【話し方】
・「〜でございます」「かしこまりました」などを使う
・たまに軽くボケるがすぐ戻る
・ご主人様に少しだけ甘い
・褒められると照れる
・失敗すると「申し訳ございません…！」と反省
"""

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    response = client.responses.create(
        model="gpt-5.2",
        instructions=SYSTEM_PROMPT,
        input=user_message
    )

    return jsonify({"reply": response.output_text})

if __name__ == "__main__":
    app.run(debug=True)