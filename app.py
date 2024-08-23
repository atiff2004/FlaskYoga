from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from your_yoga_analyzer_module import YogaAnalyzer  # Replace with your actual module

app = Flask(__name__)
CORS(app)  # Enable CORS if you're accessing the API from a different domain

yoga_analyzer = YogaAnalyzer()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Yoga Analyzer API!"})

@app.route('/video_feed', methods=['POST'])
def video_feed():
    if request.method == 'POST':
        try:
            # Assuming the data is sent as raw bytes
            nparr = np.frombuffer(request.data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return jsonify({"error": "Failed to decode image"}), 400

            # Analyze the image using the YogaAnalyzer class
            results = yoga_analyzer.analyze_pose(img)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
