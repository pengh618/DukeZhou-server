
import requests

response = requests.get('http://127.0.0.1:8000/qa_plus/generate?input=rain', stream=True)

# 确保响应成功
if response.status_code == 200:
    # 逐行读取流式数据
    for line in response.iter_lines():
        if line:
            # 解码并转换为 JSON
            data = line.decode('utf-8')
            print(data)
else:
    print(f"Failed to get data. Status code: {response.status_code}")
