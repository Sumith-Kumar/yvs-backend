from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from app.routes.summarize import summarize_bp
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    # Enable CORS (important for frontend later)
    CORS(app)

    # Register blueprints
    app.register_blueprint(summarize_bp)

    # Health check route
    @app.route("/")
    def home():
        return jsonify({
            "message": "YouTube Video Summarizer API is running 🚀"
        })

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)