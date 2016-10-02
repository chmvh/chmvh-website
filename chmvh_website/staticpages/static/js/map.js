function initializeMap() {

    var home = new google.maps.LatLng(35.879982, -79.070320);

    var mapOptions = {
        center: home,
        disableDefaultUI: true,
        draggable: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scrollwheel: false,
        zoom: 11
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    map.set('styles', [{
        featureType: 'landscape',
        elementType: 'geometry',
        stylers: [
            { hue: '#ffff00' },
            { saturation: 30 },
            { lightness: 10}
        ]}
    ]);

    var circleOptions = {
        strokeColor: '#0000FF',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#0000FF',
        fillOpacity: 0.35,
        map: map,
        center: home,
        radius: 8050
    };

    coverage = new google.maps.Circle(circleOptions);
}
