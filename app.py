from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from main import YogaAnalyzer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

yoga_analyzer = YogaAnalyzer()

@app.route('/')
def index():
    return "Flask Yoga Analyzer is running!"
    
@app.route('/video_feed', methods=['POST'])
def video_feed():
    try:
        print("Received a request")
        
        data = request.data
        if not data:
            raise ValueError("No data received")
        
        print(f"Data size: {len(data)} bytes")
        
        # Decode Base64 string into numpy array
        np_arr = np.frombuffer(base64.b64decode(data), np.uint8)
        print(f"Buffer size: {np_arr.size}")
        
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Failed to decode the image")

        analyzed_frame = yoga_analyzer.analyze_pose(frame)

        # Get the results from YogaAnalyzer after analyzing the pose
        results = yoga_analyzer.get_results()

        return jsonify(results)
    except Exception as e:
        print(f"Error processing the image: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render.com uses port 10000
    app.run(host='0.0.0.0', port=port)
