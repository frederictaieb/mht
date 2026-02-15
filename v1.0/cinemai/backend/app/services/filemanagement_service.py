import os
import uuid
import shutil
from fastapi import UploadFile, File, HTTPException

from enum import Enum

class DirectoryKind(str, Enum):
    IMG = "img"
    VID = "vid"

class DirectoryService:

    def __init__(self, dir: str, kind: str):
        self.dir = dir

        if kind == DirectoryKind.IMG:
            self.ALLOWED_MIME = {"image/jpeg", "image/png"}
            self.ALLOWED_EXT = {".jpg", ".jpeg", ".png"}

        elif kind == DirectoryKind.VID:
            self.ALLOWED_MIME = {"video/mp4", "video/webm", "video/mpeg"}
            self.ALLOWED_EXT = {".mp4",".webm",".mpg",".mpeg"}

        else:
            raise ValueError(f"Unknown kind: {kind}")

    # --- Check if folder exists ---
    def extract_ext(self, f):
        return os.path.splitext(f.filename or "")[1].lower()

    # --- Check if folder exists ---
    def check_dir(self):
        if not os.path.exists(self.dir):
            raise HTTPException(status_code=404, detail="Directory not found")

        if not os.path.isdir(self.dir):
            raise HTTPException(status_code=400, detail="Path not correct")

    # --- Check MIME of a file ---
    def check_mime(self, f):
        if f.content_type not in self.ALLOWED_MIME:
            raise HTTPException(status_code=415, detail="MIME not authorized")

    # --- Check Extension of a file ---
    def check_ext(self, ext):
        if ext not in self.ALLOWED_EXT:
            raise HTTPException(status_code=415, detail="EXT not authorized")

    # --- List all files in folder ---
    def dir_list(self):

        self.check_dir()

        # List comprehension : 
        # [ EXPRESSION  for ELEMENT in SEQUENCE  if CONDITION ]
        # I build a list containing f 
        #   For each f in SEQUENCE : os.listdir(self.dir)
        #   Only if condition: os.path.isfile(os.path.join(self.dir, f)) is true

        files = [
            f 
            for f in os.listdir(self.dir)
            if os.path.isfile(os.path.join(self.dir, f))
        ]

        return {
            "directory": self.dir,
            "type": "list",
            "count": len(files),
            "files": files
        }

    # --- Delete all files in input/img dir ---
    def dir_delete(self):
        # Counter of deletion
        deleted = 0

        self.check_dir()

        for f in os.listdir(self.dir):
            # Absolute path of the current file in img dir
            abs_f = os.path.join(self.dir, f)

            try:
                # If dir or if link cascade delete
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
            "directory": self.dir,
            "type": "delete",
            "count": deleted
        }

    # --- Upload image ---
    def dir_upload(self, f: UploadFile = File(...)):

        self.check_dir()

        # Checking Extension with split extension function
        ext = self.extract_ext(f)
        self.check_mime(f)
        self.check_ext(ext)

        # Destination file
        safe_name = f"{uuid.uuid4().hex}{ext}"
        abs_dest = os.path.join(self.dir, safe_name)

        # Writing on drive
        try:
            with open(abs_dest, "wb") as dest:
                shutil.copyfileobj(f.file, dest)
        finally:
            f.file.close()

        return {
            "directory": self.dir,
            "type": "upload",
            "filename": safe_name,
        }