// Despliega cada menu al hacer click en el signo "+" y lo cierra al hacer click en el signo "-"
function showAndHide(param){
    var selection = document.getElementById(param);  
    if (selection.style.display == 'none') {
        selection.style.display = 'block';
    } else {
        selection.style.display = 'none';
    }
    let prevSiblings = selection.previousElementSibling;
    let icon = prevSiblings.children[1];
    if(icon.innerHTML == "+"){
        icon.innerHTML = "-"
    }
    else{
        icon.innerHTML = "+"
    }
}
// Al elegir un radio button muestra un parrafo con el detalle del servicio
function showRadioButtonDiv (idBaseName, numberOfButtons) {
    for (x=1;x<=numberOfButtons;x++) {
        checkThisButton = idBaseName + x;
        thisDiv = idBaseName + x +'Div';
    if (document.getElementById(checkThisButton).checked) {
        document.getElementById(thisDiv).style.display = "block";
        }
    else {
        document.getElementById(thisDiv).style.display = "none";
        }
    }
    return false;
}
// Funcion para obtener los datos ingresados en cada campo para posteriormente ser mostrados al usuario y pedir su confirmacion (NO FUNCIONAL)
function getData(form) {
    var formData = new FormData(form);
    console.log(Object.fromEntries(formData));
}
document.getElementById("myForm").addEventListener("submit", function (e) {
    e.preventDefault();
    getData(e.target);
});

// MODAL Bootstrap (ver sweet-alerts)
const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
    myInput.focus()
})