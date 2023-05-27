$.getJSON('/agency/00dc6466bcfab2a257c86bd6076fa60baf03863c', function(data) {
    document.getElementById("name").innerHTML = (data.name);
    document.getElementById("description").innerHTML = (data.description);
    var type = document.createTextNode(data.type);
    var tag = document.getElementById("tags");
    tag.appendChild(type);
    document.getElementById("adresse").innerHTML = (data.adresse);
    let i = 0;
    data.schedules.forEach(d => {
        if (d.Openning) {
            let morn = document.querySelectorAll('.matin td');
            morn[i].innerHTML = d["Openning"] == null ? "Closed" : d["Openning"]+"h";
     
            morn[i].setAttribute("style", "color:#000000");

            let aftn = document.querySelectorAll('.aprem td');
            aftn[i].setAttribute("style", "color:#000000");
            aftn[i].innerHTML = d["Closing"] == null ? "Closed" : d["Closing"]+"h";
        }
        else {
            let morn = document.querySelectorAll('.matin td');
            morn[i].setAttribute("style", "color:#FF8133");

            let aftn = document.querySelectorAll('.aprem td');
            aftn[i].setAttribute("style", "color:#FF8133");
        }
        i++;
    }); 
    
    
});

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
