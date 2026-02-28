import threading
import time

from flask import Flask, send_file, jsonify, request
from werkzeug.serving import make_server

# 存储最新心率数据（线程安全，避免多请求冲突）
heart_rate_data = {
    "heart_rate": 0,  # 心率值（次/分钟）
    "timestamp": 0,  # 数据更新时间戳
    "device_id": "unknown"  # 设备ID（可选）
}
data_lock = threading.Lock()

app = Flask(__name__)  # 创建 Flask 应用实例


@app.route('/')
def index():
    """首页：展示实时心率数据"""
    return send_file('../index.html')


@app.route('/api/heart_rate', methods=['GET'])
def get_heart_rate():
    """获取最新心率数据的接口（HTTP 广播核心接口）"""
    time.sleep(2)
    with data_lock:
        return jsonify(heart_rate_data)


@app.route('/api/heart_rate', methods=['POST'])
def update_heart_rate():
    """上传/更新心率数据的接口"""
    try:
        # 获取上传的JSON数据
        data = request.get_json()
        print(data)
        if not data or 'heart_rate' not in data:
            return jsonify({"error": "缺少心率数据"}), 400

        # 验证心率值合法性
        heart_rate = int(data['heart_rate'])
        if heart_rate < 0 or heart_rate > 250:
            return jsonify({"error": "心率值超出合理范围"}), 400

        # 线程安全更新数据
        with data_lock:
            heart_rate_data['heart_rate'] = heart_rate
            heart_rate_data['timestamp'] = data['timestamp']
            heart_rate_data['device_id'] = data['device_id']

        return jsonify({"success": True, "data": heart_rate_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 定义服务器类，封装启动/停止逻辑
class FlaskServer:
    def __init__(self, app):
        self.server = make_server('127.0.0.1', 5001, app)
        self.thread = threading.Thread(target=self.server.serve_forever)

    def start(self):
        self.thread.start()
        print('Flask服务器已启动 (http://127.0.0.1:5001)')

    def stop(self):
        # 停止服务器
        self.server.shutdown()
        # 等待线程结束
        self.thread.join()
        print("Flask服务器已停止")


# 测试代码
if __name__ == '__main__':
    server = FlaskServer(app)
    server.start()
    # time.sleep(1)
    # server.stop()
