import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        if not file:
            return func.HttpResponse("un fichier manquant", status_code=400)

        conn = os.environ["AzureWebJobsStorage"]
        bsc = BlobServiceClient.from_connection_string(conn)

        container = bsc.get_container_client("mesimages")
        container.upload_blob(file.filename, file.stream, overwrite=True)

        return func.HttpResponse("Upload avec succes ", status_code=200)

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)