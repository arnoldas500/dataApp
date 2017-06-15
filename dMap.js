
var dextent = ol.proj.transformExtent(
    [-81.00, 40.0, -72.00, 46.0],
    'EPSG:4326', 'EPSG:3857'
);

var dBase = new ol.layer.Tile({
        source: new ol.source.OSM()
});
 
var dview = new ol.View({
   center: ol.proj.transform([-76.1474, 41.991],
            'EPSG:4326', 'EPSG:3857'),
    zoom: 6,
    minZoom: 5,
    //extent: dextent
});

var dispmap = new ol.Map({
    layers: [dBase],
    target: 'dispmap',
    view: dview
});



