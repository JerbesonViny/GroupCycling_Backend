import os
from werkzeug.utils import secure_filename
from app import client

def upload_file_to_s3(file, filename, acl="private"):
  file_name = secure_filename(filename)
  try:
    client.upload_fileobj(
      file,
      os.getenv("AWS_BUCKET_NAME"),
      f"image-upload/{file_name}",
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print("Something Happened: ", e)
    return e
    

  # after upload file to s3 bucket, return filename of the uploaded file
  return file_name
  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# function to check file extension
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS