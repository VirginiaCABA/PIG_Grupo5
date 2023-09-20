function initMap() {
    const coord = { lat: -34.6037389, lng: -58.3815704 }
    const map = new google.maps.Map(mapDiv, {
        center: coord,
        zoom: 15,
    });
    
    const marker = new google.maps.Marker({
        position: coord,
        map: map
    })
}


