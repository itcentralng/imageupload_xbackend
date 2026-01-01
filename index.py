import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER_TWEET = os.path.join("/tmp", os.getenv("UPLOAD_DEST_TWEET"))
UPLOAD_FOLDER_PROFILE = os.path.join("/tmp", os.getenv("UPLOAD_DEST_PROFILE"))
UPLOAD_FOLDER_COVERPROFILE = os.path.join("/tmp", os.getenv("UPLOAD_DEST_COVERPHOTO"))

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
@app.route('/tweetimage', methods=['POST'])
def tweetuploadfile():
    try:
        if 'files' not in request.files:
            return jsonify({
                "status": "failed",
                "message": "No files part in request"
            }), 400

        files = request.files.getlist('files')

        if not files or len(files) == 0:
            return jsonify({
                "status": "failed",
                "message": "No files provided"
            }), 400

        upload_dir = app.config.get('UPLOAD_FOLDER_TWEET')

        if not upload_dir:
            return jsonify({
                "status": "failed",
                "message": "Upload directory not configured"
            }), 500

        os.makedirs(upload_dir, exist_ok=True)

        urls = []

        for file in files:
            if not file or file.filename.strip() == "":
                continue

            if not allowed_file(file.filename):
                continue

            filename = secure_filename(file.filename)

            # prevent filename collision
            # unique_name = f"{uuid.uuid4().hex}_{filename}"

            save_path = os.path.join(upload_dir, filename)
            file.save(save_path)

            urls.append(f"/tweetimage/{filename}")

        if len(urls) == 0:
            return jsonify({
                "status": "failed",
                "message": "No valid images uploaded"
            }), 400

        return jsonify({
            "status": "success",
            "message": "Tweet images uploaded",
            "urls": urls
        }), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "Error uploading files",
            "reason": str(e)
        }), 500

@app.route('/profile', methods=['GET', 'POST'])
def profileuploadfile():
    try:
        if 'files' not in request.files:
            return jsonify({
                "status": "failed",
                "message": "No files part in request"
            }), 400

        files = request.files.get('file')

        if not files or len(files) == 0:
            return jsonify({
                "status": "failed",
                "message": "No files provided"
            }), 400

        upload_dir = app.config.get('UPLOAD_FOLDER_PROFILE')

        if not upload_dir:
            return jsonify({
                "status": "failed",
                "message": "Upload directory not configured"
            }), 500

        os.makedirs(upload_dir, exist_ok=True)

        urls = []

        for file in files:
            if not file or file.filename.strip() == "":
                continue

            if not allowed_file(file.filename):
                continue

            filename = secure_filename(file.filename)

            # prevent filename collision
            # unique_name = f"{uuid.uuid4().hex}_{filename}"

            save_path = os.path.join(upload_dir, filename)
            file.save(save_path)

            urls.append(f"/tweetimage/{filename}")

        if len(urls) == 0:
            return jsonify({
                "status": "failed",
                "message": "No valid images uploaded"
            }), 400

        return jsonify({
            "status": "success",
            "message": "Tweet images uploaded",
            "urls": urls
        }), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": "Error uploading files",
            "reason": str(e)
        }), 500

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
            save_path = os.path.join(app.config.get('UPLOAD_FOLDER_COVERPROFILE'), filename)
            file.save(save_path)
            coverimage_url = (f"/coverimage/{filename}")
        return jsonify({"status":"success", "message":"coverprofile uploaded", "urls":coverimage_url}) , 200
        
#--- This is to get the tweet 
@app.route('/tweetimage/<filename>', methods=["GET"])
def tweet_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_TWEET'], filename)

#--- This is for the profile pic
@app.route('/profileimg/<filename>', methods=["GET"])
def profile_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_PROFILE'], filename)

#--- This is for the cover photo
@app.route('/coverprofile/<filename>', methods=["GET"])
def cover_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_COVERPROFILE'], filename)



if __name__ == "__main__":
    print("The image upload backend is running...")
    app.run(debug=True)