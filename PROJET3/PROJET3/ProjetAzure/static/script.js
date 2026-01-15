// =========================
// CONSTANTE DE BASE
// =========================

// URL de base de ton Azure Function App
const FUNCTION_BASE_URL = "https://sane-hzdzbkgwb2fvbbbz.canadacentral-01.azurewebsites.net";


// =========================
// RÉCUPÉRATION DES ÉLÉMENTS DU DOM
// =========================

// Input de sélection de fichier
const fileInput = document.getElementById("filename");

// Élément HTML pour afficher les messages de statut
const statusEl = document.getElementById("fichiersredimendione");

// Container pour afficher les miniatures
const grid = document.getElementById("gridsize");


// =========================
// FONCTION D’AFFICHAGE DE STATUT
// =========================
function setStatus(msg) {
  // Met à jour le contenu texte de l’élément statusEl
  statusEl.textContent = msg;
}


// =========================
// UPLOAD IMAGE
// =========================

// Ajouter un écouteur d'événement sur le bouton "Upload"
document.getElementById("uploadBtn").addEventListener("click", async () => {

  // Récupérer le fichier sélectionné
  const file = fileInput.files[0];

  // Vérifier qu’un fichier a été choisi
  if (!file) {
    setStatus("Choisis une image d'abord.");
    return;
  }

  // Créer un objet FormData pour envoyer le fichier
  const formData = new FormData();
  formData.append("file", file);

  // Mettre à jour le statut pendant l’upload
  setStatus("Upload en cours...");

  try {
    // Appel HTTP POST vers la fonction Azure pour uploader le fichier
    const res = await fetch(`${FUNCTION_BASE_URL}/uploadimage`, {
      method: "POST",
      body: formData
    });

    // Récupérer la réponse textuelle
    const txt = await res.text();

    // Si le serveur retourne une erreur
    if (!res.ok) {
      setStatus("Erreur upload : " + txt);
      return;
    }

    // Si tout s’est bien passé
    setStatus("Téléchargement fait avec succès");

  } catch (err) {
    // Gestion des erreurs réseau ou autres exceptions
    setStatus("Erreur de réseau : " + err.message);
  }
});


// =========================
// LISTE DES MINIATURES
// =========================

// Ajouter un écouteur sur le bouton "List"
document.getElementById("listBtn").addEventListener("click", async () => {

  // Mettre à jour le statut pendant le chargement
  setStatus("En cours de chargement des miniatures...");

  // Vider le container des images existantes
  grid.innerHTML = "";

  try {
    // Appel HTTP GET vers la fonction Azure pour récupérer la liste des images
    const res = await fetch(`${FUNCTION_BASE_URL}/listimage`);

    // Vérification de la réponse
    if (!res.ok) {
      const txt = await res.text();
      setStatus("Erreur : " + txt);
      return;
    }

    // Convertir la réponse JSON en tableau
    const mesimages = await res.json();

    // Vérifier s’il y a des images
    if (mesimages.length === 0) {
      setStatus("Pas de miniature disponible");
    } else {
      setStatus(`Affichage : ${mesimages.length} miniatures`);
    }

    // Pour chaque URL d’image, créer un élément <img> et l’ajouter à la grille
    mesimages.forEach(url => {
      const img = document.createElement("img");
      img.src = url;        // Source de l’image
      img.width = 150;      // Largeur fixe pour miniatures
      grid.appendChild(img); // Ajouter l’image à l’élément grid
    });

  } catch (err) {
    // Gestion des erreurs réseau ou exceptions
    setStatus("Erreur de réseau : " + err.message);
  }
});
