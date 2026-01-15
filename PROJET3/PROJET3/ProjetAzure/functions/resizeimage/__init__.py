import os
import io
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError
from PIL import Image

def main(myblob: func.InputStream):
    try:
        size = int(os.getenv("THUMB_SIZE", "256"))
        thumbs_container = os.getenv("THUMBS_CONTAINER", "fichiersredimendione")

        # Utiliser la même connexion que le trigger
        conn = os.environ["AzureWebJobsStorage"]
        bsc = BlobServiceClient.from_connection_string(conn)

        # Créer le container thumbs si nécessaire
        try:
            bsc.create_container(thumbs_container)
        except ResourceExistsError:
            pass

        # Nom du blob d'entrée (robuste)
        blob_full = myblob.name  # ex: "images/raw.jpg" ou "raw.jpg"
        blob_name = blob_full.split("/", 1)[1] if "/" in blob_full else blob_full

        # Lire l'image directement depuis le stream du trigger
        data = myblob.read()

        img = Image.open(io.BytesIO(data))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.thumbnail((size, size))

        out_name = f"{os.path.splitext(blob_name)[0]}_{size}.jpg"

        out = io.BytesIO()
        img.save(out, format="JPEG", quality=85)
        out.seek(0)

        out_client = bsc.get_blob_client(container=fichiersredimendione_container, blob=out_name)
        out_client.upload_blob(
            out,
            overwrite=True,
            content_settings=ContentSettings(content_type="mesimage/jpeg")
        )

        logging.info(f"fichiersredimendione created: {thumbs_container}/{out_name}")

    except Exception:
        logging.exception("generatefichiersredimendione error")
        raise