from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# Copyright © 2021 Markus W Mahlberg
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.
from minio import Minio
import os,io

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = { 'png', 'jpg', 'jpeg', 'gif'}
app.config['MINIO'] = os.getenv("MINIO","localhost:9000")
app.config['PREFIX'] = os.getenv("MINIO_PREFIX","http://localhost:9000/images")

client = Minio(app.config['MINIO'],
      secure=False,
      access_key=os.getenv("MINIO_ROOT_USER","minio"),
      secret_key=os.getenv("MINIO_ROOT_PASSWORD","minio123"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
  if not client.bucket_exists("images"):
    print("Foo")
    return render_template('error.html',
      status_text="Internal Server Error",
      msg="Bucket \"images\" does not exist!",
      code=500,
      ), 500
  images = client.list_objects("images")
  return render_template('index.html',prefix=app.config['PREFIX'],images=images)

@app.route("/upload",methods=['POST'])
def upload_file():

  if 'file' not in request.files:
    flash('No file!')
    return redirect(request.url)

  file = request.files['file']

  if file.filename == '':
    flash('No selected file')
    return redirect("/")

  if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      result = client.put_object(
        bucket_name="images",
        object_name=filename,
        data=file.stream,
        length=-1,
        part_size=10*1024*1024,
        content_type=file.content_type)
      print("Uploaded %s with etag %s to minio",filename,result.etag)
      return redirect("/")
  return redirect("/")
if __name__ == "__main__":
    app.run(host=os.getenv("APP_HOST","127.0.0.1"),port=os.getenv("APP_PORT",5000))

