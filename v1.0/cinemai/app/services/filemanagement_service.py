import os

class ImageService:

    ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}

    def __init__(self, img_dir: str):
        self.img_dir = img_dir

    def check_img_dir(self):
        if not os.path.exists(self.img_dir):
            raise HTTPException(status_code=404, detail="Dossier img introuvable")

        if not os.path.isdir(self.img_dir):
            raise HTTPException(status_code=400, detail="Le chemin n'est pas un dossier")

    def img_list(self):
        self.check_img_dir()

        files = [
            f for f in os.listdir(self.img_dir)
            if os.path.isfile(os.path.join(self.img_dir, f))
        ]

        return {
            "directory": self.img_dir,
            "count": len(files),
            "files": files
        }

    def img_delete(self):
        deleted = 0

        self.check_img_dir()

        for filename in os.listdir(self.img_dir):
            path = os.path.join(self.img_dir, filename)

            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                    deleted += 1
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    deleted += 1
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")

        return {
            "message": "input directory cleared",
            "deleted_items": deleted
        }