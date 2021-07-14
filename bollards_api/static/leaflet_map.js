//Leaflet setup at
//https://leafletjs.com/examples/quick-start/

//Retrieved from
//https://codepen.io/geoadmin/pen/JKAjWk?editors=0010
//https://api3.geo.admin.ch/api/examples.html
var myBollardMap = new L.Map('bollardmap', {
    crs: L.CRS.EPSG3857,
    continuousWorld: true,
    worldCopyJump: false
});
var url = 'https://wmts20.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg';
var tilelayer = new L.tileLayer(url);
myBollardMap.addLayer(tilelayer);
myBollardMap.setView(L.latLng(46.64692, 6.28342), 9);

var position_marker = L.marker([46.64692, 6.28342]).addTo(myBollardMap);


function onMapClick(e) {
    //Update the values of coordinate fields
    document.getElementById('manage-b-lat').value = e.latlng.lat;
    document.getElementById('manage-b-lon').value = e.latlng.lng;

    //update the marker position
    position_marker.setLatLng(e.latlng)
}

myBollardMap.on('click', onMapClick);