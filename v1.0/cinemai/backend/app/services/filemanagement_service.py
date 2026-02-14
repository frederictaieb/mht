import os
import uuid
import shutil
from fastapi import UploadFile, File, HTTPException

class ImageService:

    ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}

    def __init__(self, img_dir: str):
        self.img_dir = img_dir

    # --- Check if img folder exists ---
    def check_img_dir(self):
        if not os.path.exists(self.img_dir):
            raise HTTPException(status_code=404, detail="Dossier img introuvable")

        if not os.path.isdir(self.img_dir):
            raise HTTPException(status_code=400, detail="Le chemin n'est pas un dossier")

    # --- List all files in input/img folder ---
    def img_list(self):

        self.check_img_dir()

        # List comprehension : 
        # [ EXPRESSION  for ELEMENT in SEQUENCE  if CONDITION ]
        # I build a list containing f 
        #   For each f in SEQUENCE : os.listdir(self.img_dir)
        #   Only if condition: os.path.isfile(os.path.join(self.img_dir, f)) is true

        files = [
            f 
            for f in os.listdir(self.img_dir)
            if os.path.isfile(os.path.join(self.img_dir, f))
        ]

        return {
            "directory": self.img_dir,
            "type": "list",
            "count": len(files),
            "files": files
        }

    # --- Delete all files in input/img folder ---
    def img_delete(self):
        # Counter of deletion
        deleted = 0

        self.check_img_dir()

        for f in os.listdir(self.img_dir):
            # Absolute path of the current file in img folder
            abs_f = os.path.join(self.img_dir, f)

            try:
                # If folder or if link cascade delete
                if os.path.isdir(abs_f) and not os.path.islink(abs_f):
                    shutil.rmtree(abs_f)
                else:
                    #Else delete
                    os.unlink(abs_f)
                # Increments counter
                deleted += 1
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")

        return {
            "directory": self.img_dir,
            "type": "delete",
            "count": deleted
        }

    # --- Upload image ---
    def img_upload(self, f: UploadFile = File(...)):
        ALLOWED_MIME = {"image/jpeg", "image/png"}
        ALLOWED_EXT = {".jpg", ".jpeg", ".png"}

        # Checking Extension with split extension function
        ext = os.path.splitext(f.filename or "")[1].lower()

        if f.content_type not in ALLOWED_MIME:
            raise ValueError("File has to be jpg, jpeg or png")

        if ext not in ALLOWED_EXT:
            raise ValueError("Incorrect file extension")

        # Destination file
        safe_name = f"{uuid.uuid4().hex}{ext}"
        abs_dest = os.path.join(self.img_dir, safe_name)

        # Writing on drive
        try:
            with open(abs_dest, "wb") as dest:
                shutil.copyfileobj(f.file, dest)
        finally:
            f.file.close()

        return {
            "directory": self.img_dir,
            "type": "upload",
            "filename": safe_name,
        }