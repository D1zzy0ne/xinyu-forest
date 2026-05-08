# tts.py —— 比赛最终版（语速正常、国内可用）
import edge_tts
import asyncio
import io

async def voice(text):
    com = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+20%")
    data = io.BytesIO()
    async for chunk in com.stream():
        if chunk["type"] == "audio":
            data.write(chunk["data"])
    data.seek(0)
    return data.read()

def text_to_speech(text):
    return asyncio.run(voice(text))
