# =========================
# IMPORTS
# =========================
import azure.functions as func                 # Pour créer des fonctions Azure HTTP
from azure.storage.blob import BlobServiceClient  # Pour interagir avec Azure Blob Storage
import os                                     # Pour accéder aux variables d'environnement
import json                                   # Pour manipuler les objets JSON


# =========================
# FONCTION PRINCIPALE
# =========================
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Fonction Azure HTTP Trigger qui liste toutes les images
    dans le container 'fichiersredimendione' et retourne
    un tableau JSON contenant leurs URLs complètes.
    """

    # Récupération de la chaîne de connexion au compte de stockage depuis les variables d'environnement
    conn = os.environ["AzureWebJobsStorage"]

    # Création d'un client BlobService pour interagir avec le stockage Azure
    bsc = BlobServiceClient.from_connection_string(conn)

    # Sélection du container spécifique où sont stockées les images
    container = bsc.get_container_client("fichiersredimendione")

    # Liste qui contiendra les URLs complètes de chaque blob (image) du container
    urls = []

    # Parcourir tous les blobs (fichiers) dans le container
    for blob in container.list_blobs():
        # Construire l'URL complète de chaque fichier et l'ajouter à la liste
        urls.append(f"{container.url}/{blob.name}")

    # Retourner une réponse HTTP contenant le JSON des URLs
    return func.HttpResponse(
        json.dumps(urls),          # Conversion de la liste Python en JSON
        mimetype="application/json",  # Type MIME de la réponse
        status_code=200             # Code HTTP 200 = OK
    )
