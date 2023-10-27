// function registro() {
//     let name = document.getElementById("name").value;
//     let apellido = document.getElementById("lastname").value;
//     let email = document.getElementById("email").value;
//     let password = document.getElementById("password").value;
//     let password2 = document.getElementById("password2").value;
//     if ( password === password2 ) {
//         alert("clave correcta")
//     } else {
//         alert("La contraseña no coincide")
//     }
// }

// function registro() {
//     const $form = document.querySelector('#form')
//     const $buttonMailto = document.querySelector('#correo')

//     $form.addEventListener('submit', handleSubmit)

//     function handleSubmit(event) {
//         event.preventDefault()
//         const form = new FormData(this)
//         console.log(form.get('NombreDeUsuario'))
//         $buttonMailto.setAttribute('href', `mailto:virginiav@gmail.com?subject=nombre: ${form.get('NombreDeUsuario')} correo: ${form.get('email')}&body=${form.get('message')}`)
//         $buttonMailto.click()
//     }

// }

function registro() {
    let name = document.getElementById("name").value;
    let apellido = document.getElementById("lastname").value;
    let email = document.getElementById("email").value;
    let emailValidate = /[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z]{2,4}/
    let dni = document.getElementById("DNI").value;
    let message = document.getElementById("message").value;
    let file = document.getElementById("file").value;

    if (name.length > 1) {
        document.getElementById('errorName').style.display="none";
    } else {
        document.getElementById('errorName').style.display="block";
        return 1;
    }
    if (apellido.length > 1) {
        document.getElementById('errorLastname').style.display="none";
    } else {
        document.getElementById('errorLastname').style.display="block";
        return 1;
    }
    if (dni.length > 7 && parseInt(dni) > 0) {
        document.getElementById('errorDNI').style.display="none";
    } else {
        document.getElementById('errorDNI').style.display="block";
        return 1;
    }
    if (emailValidate.test(email)) {
        document.getElementById('errorMail').style.display="none";
    } else {
        document.getElementById('errorMail').style.display="block";
        return 1;
    }
    if (message.length > 1) {
        document.getElementById('errorMSG').style.display="none";
    } else {
        document.getElementById('errorMSG').style.display="block";
        return 1;
    }
    if (file.length > 1) {
        document.getElementById('errorFile').style.display="none";
    } else {
        document.getElementById('errorFile').style.display="block";
        return 1;
    }



    const $form = document.querySelector('#form')
    const $buttonMailto = document.querySelector('#correo')

    $form.addEventListener('submit', handleSubmit)

    function handleSubmit(event) {
        event.preventDefault()
        const form = new FormData(this)
        console.log(form.get('NombreDeUsuario'))
        $buttonMailto.setAttribute('href', `mailto:virginiav@gmail.com?subject=nombre: ${form.get('NombreDeUsuario')} correo: ${form.get('email')}&body=${form.get('message')}`)
        $buttonMailto.click()
    }

}
