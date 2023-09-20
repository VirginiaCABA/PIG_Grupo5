let footer = document.getElementById('footer');
let select = window.location.pathname

footer.innerHTML = `
<footer class="footer">
<h6>&copy; Codo a Codo 2023. Todos los derechos reservados. </h6>
<nav class="footer_nav">
    <ul class="footer_links">
        <li class="footer_list"><a href="#"><img src="${select.includes("index.html") ? "static/core/img/whatsapp.png" : "../static/core/img/whatsapp.png"}" alt="logo whatsapp"></a></li>
        <li class="footer_list"><a href="#"><img src="${select.includes("index.html") ? "static/core/img/facebook.png" : "../static/core/img/facebook.png"}" alt="logo facebook"></a></li>
        <li class="footer_list"><a href="#"><img src="${select.includes("index.html") ? "static/core/img/instagram.png" : "../static/core/img/instagram.png"}" alt="logo instagram"></a></li>
        <li class="footer_list"><a href="#"><img src="${select.includes("index.html") ? "static/core/img/telegram.png" : "../static/core/img/telegram.png"}" alt="logo telegram"></a></li>
    </ul>
</nav>
</footer>`
