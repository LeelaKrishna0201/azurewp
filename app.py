from flask import Flask, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection from environment variables
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["feedbackdb"]
collection = db["feedback"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        collection.insert_one({"name": name, "message": message})
    
    feedbacks = collection.find()
    return render_template("index.html", feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
