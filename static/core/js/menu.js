let menu = document.getElementById('menu');
let select = window.location.pathname
let active=`class="active"`

menu.innerHTML = `
{% load static %}
<nav class="contenedor">
<div class="logo">
    <a href="/">
        <img class="header_logo" src="{% static 'core/img/logo.png' %}" alt="logo">
        <h1 class="menu">CODO A CODO Logística</h1>
    </a>
</div>

<ul class="header_links">
    <li class="header_list"><a ${select === "/" ? active : ""} href="/">Inicio</a></li>
    <li class="header_list"><a ${select.includes("nosotros") ? active : ""} href="/nosotros/">Nosotros</a></li>
    <li class="header_list"><a ${select.includes("servicios") ? active : ""} href="/servicios/">Servicios</a></li>
    <li class="header_list"><a ${select.includes("contacto") ? active : ""} href="/contacto/">Contacto</a></li>
    <li class="header_list"><a ${select.includes("clientes") ? active : ""} href="/clientes/">Clientes</a></li>
</ul>
</nav>`


