from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for likes and comments
likes = {}
comments = {}

@app.route('/')
def home():
    # List images in the upload folder
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', images=images, likes=likes, comments=comments)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # Initialize likes and comments for the new image
        likes[file.filename] = 0
        comments[file.filename] = []
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/like/<filename>', methods=['POST'])
def like_photo(filename):
    if filename in likes:
        likes[filename] += 1
    return jsonify({"likes": likes[filename]})

@app.route('/comment/<filename>', methods=['POST'])
def comment_photo(filename):
    if filename in comments:
        comment_text = request.form.get('comment')
        if comment_text:
            comments[filename].append(comment_text)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
