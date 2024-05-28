document.addEventListener('DOMContentLoaded', function() {
    var image_modal = document.getElementById('Modal_for_image'); //Récupération du modal de la page image.html
    image_modal.addEventListener('show.bs.modal', function(event) {
        var image = event.relatedTarget; //récupération de l'élément image cliquée 
        var image_src = image.getAttribute('data-bs-image-src'); //Récupération du data-bs-image-src, liée à l'image cliquable, soit le lien de la vignette dans le dossier media
        var image_in_modal = image_modal.querySelector('.modal-body img'); //Situe l'endroit où va être affichée l'image dans le modal
        image_in_modal.src = image_src; //La source de l'image dans le modal est remplacée par le lien de l'image cliquable
    });
});