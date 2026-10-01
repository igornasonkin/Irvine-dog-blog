import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ensure the upload folder exists securely on the server
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for the live discussion state
blog_state = {
    "topic": "Welcome to our new interactive dog blog!",
    "characters": [
        {"name": "Mark", "gender": "male", "role": "Head Trainer", "initials": "M"},
        {"name": "Chloe", "gender": "female", "role": "Nutritional Expert", "initials": "C"}
    ],
    "dialogue": [
        {"speaker": "Mark", "initials": "M", "text": "Hey everyone! Welcome to our brand new interactive dog space. Drop a topic or link, and let's talk pups!"},
        {"speaker": "Chloe", "initials": "C", "text": "I'm so excited. Whether it's nutrition, local park meetups, or product reviews, we're diving straight in."}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', state=blog_state)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(blog_state)

@app.route('/api/ingest', methods=['POST'])
def ingest_material():
    """Ingests uploaded files, notes, or YouTube links from your phone/desktop."""
    notes = request.form.get('notes', '')
    yt_url = request.form.get('youtube_url', '')
    file = request.files.get('media')
    
    if file and file.filename:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
    # AI integration placeholder: generates multi-voice responses based on your uploads
    new_exchanges = [
        {"speaker": "Mark", "initials": "M", "text": f"Just reviewed the new material submitted: {notes or yt_url}. This is huge for local dog owners!"},
        {"speaker": "Chloe", "initials": "C", "text": "Completely agree, Mark. Let's break down the practical takeaways for our community."}
    ]
    blog_state["dialogue"].extend(new_exchanges)
    return jsonify({"status": "success", "dialogue": blog_state["dialogue"]})

@app.route('/api/interject', methods=['POST'])
def interject():
    """Allows website visitors to interject live and get character reactions."""
    data = request.json
    user_comment = data.get('comment', '')
    
    blog_state["dialogue"].append({"speaker": "You (Site Owner)", "initials": "YOU", "text": user_comment})
    blog_state["dialogue"].append({
        "speaker": "Mark", 
        "initials": "M", 
        "text": f"Great point joining the chat! Regarding your thought on '{user_comment}': we always emphasize safety and balance first."
    })
    return jsonify({"status": "success", "dialogue": blog_state["dialogue"]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
