import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import YogaAnalyzer  # Assuming this is in a separate file `yoga_analyzer.py`

app = Flask(__name__)
CORS(app)

# Initialize the YogaAnalyzer
yoga_analyzer = YogaAnalyzer()

@app.route('/')
def index():
    return "Flask Yoga Analyzer is running!"

@app.route('/video_feed', methods=['POST'])
def video_feed():
    try:
        # Get the image file from the request
        if 'image' not in request.files:
            return jsonify({"error": "No image file in the request"}), 400
        
        image_file = request.files['image'].read()
        np_arr = np.frombuffer(image_file, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Analyze the pose using YogaAnalyzer
        analysis_results = yoga_analyzer.analyze_pose(img)
        
        # Return the results as a JSON response
        return jsonify(analysis_results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render.com uses port 10000
    app.run(host='0.0.0.0', port=port)
