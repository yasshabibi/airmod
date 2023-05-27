function openForm() {
    document.getElementById("popupForm").style.display = "block";
  }

function closeForm() {
    document.getElementById("popupForm").style.display = "none";
  }

  function confirmation() {
    var nom = document.modification.name.value;
    var prenom = document.modification.firstname.value;
    var pseudo = document.modification.pseudo.value;
    var age = document.modification.age.value;
    var adresse = document.modification.adresse.value;
    var tel = document.modification.tel.value;

    var nom_profil = document.getElementById("nom_profil") ;
    var age_profil = document.getElementById("age_profil") ;
    var adresse_profil = document.getElementById("adresse_profil") ;
    var tel_profil = document.getElementById("tel_profil") ;

    nom_profil.innerHTML = prenom + " " + nom;
    adresse_profil.innerHTML = adresse;
    tel_profil.innerHTML = tel;

    if (age == ""){
      age_profil.innerHTML = " ";
    }else {
    age_profil.innerHTML = age + " ans";
    }
  }

  $.getJSON('/orders/1', function(data) {
    document.getElementById("qrcode").innerHTML = '<img src="/qrcodeGen?content=987654321.png">';
  });