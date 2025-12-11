import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER_TWEET = os.getenv("UPLOAD_DEST_TWEET")
UPLOAD_FOLDER_PROFILE = os.getenv("UPLOAD_DEST_PROFILE")
UPLOAD_FOLDER_COVERPROFILE = os.getenv("UPLOAD_DEST_COVERPHOTO")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER_TWEET'] = UPLOAD_FOLDER_TWEET
app.config['UPLOAD_FOLDER_PROFILE'] = UPLOAD_FOLDER_PROFILE
app.config['UPLOAD_FOLDER_COVERPROFILE'] = UPLOAD_FOLDER_COVERPROFILE

app.secret_key = os.getenv("SECRET_KEY")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/' , methods=['GET'])
def imagehome():
    return jsonify({"message":"Welcome to the image backend!!"}), 200
@app.route('/tweetimage', methods=['GET', 'POST'])
def tweetuploadfile():
    if request.method == 'POST':
        # check if the post request has the file part
        urls = []
        file = request.files.get('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename.strip() == '':
            flash('No selected file')
            return jsonify({"Message":"Sorry no selected file"}), 400
            

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER_TWEET'], filename)
            file.save(save_path)
            urls.append(f"/tweetimage/{filename}")

        return jsonify({"status":"success", "message":"tweet image uploaded", "urls":urls}) , 200
    

@app.route('/profile', methods=['GET', 'POST'])
def profileuploadfile():
    if request.method == 'POST':
        # check if the post request has the file part
        profile_url: str = ""
        file = request.files.get('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename.strip() == '':
            flash('No selected file')
            return jsonify({"Message":f"Sorry no selected file {str(file)}"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename)
            file.save(save_path)
            profile_url = (f"/profileimg/{filename}")
        return jsonify({"status":"success", "message":"profile uploaded", "urls":profile_url}) , 200
    

@app.route('/coverimage', methods=['GET', 'POST'])
def coverprofileupoadfile():
    if request.method == 'POST':
        # check if the post request has the file part
        coverimage_url: str = ""
        file = request.files.get('file')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename.strip() == '':
            flash('No selected file')
            return jsonify({"Message":"Sorry no selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER_COVERPROFILE'], filename)
            file.save(save_path)
            coverimage_url = (f"/coverimage/{filename}")
        return jsonify({"status":"success", "message":"coverprofile uploaded", "urls":coverimage_url}) , 200
        
#--- This is to get the tweet 
@app.route('/tweetimage/<filename>', methods=["GET"])
def tweet_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_TWEET'], filename)

#--- This is for the profile pic
@app.route('/profile/<filename>', methods=["GET"])
def profile_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_PROFILE'], filename)

#--- This is for the cover photo
@app.route('/coverprofile/<filename>', methods=["GET"])
def cover_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_COVERPROFILE'], filename)



if __name__ == "__main__":
    print("The image upload backend is running...")
    app.run(debug=True)