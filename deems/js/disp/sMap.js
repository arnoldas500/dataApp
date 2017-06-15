
var sextent = ol.proj.transformExtent(
    [-81.00, 40.0, -72.00, 46.0],
    'EPSG:4326', 'EPSG:3857'
);

var sBase = new ol.layer.Tile({
        source: new ol.source.OSM()
});

var sview = new ol.View({
    center: ol.proj.transform([-76.1474, 41.991],
            'EPSG:4326', 'EPSG:3857'),
    zoom: 6,
    minZoom: 5,
    extent: sextent
});

    // Set up HYSPLIT location markers as a vector layer on sele-map
    var locFeatures=[];

    var BUFFfeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([-78.76717, 43.00017],
                'EPSG:4326','EPSG:3857')),
        name: 'BUFF'
    });

    var QUEEfeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([-73.815856, 40.734335],
                'EPSG:4326','EPSG:3857')),
        name: 'QUEE'
    });
    
    var VOORfeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([-73.97562, 42.65242],
                'EPSG:4326','EPSG:3857')),
        name: 'VOOR'
    });
    
    var TUPPfeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([-74.43826, 44.22128],
                'EPSG:4326','EPSG:3857')),
        name: 'TUPP'
    });

    var WFMBfeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([-73.858829, 44.393236],
                'EPSG:4326','EPSG:3857')),
        name: 'WFMB'
    });

    locFeatures.push(BUFFfeature);
    locFeatures.push(QUEEfeature);
    locFeatures.push(VOORfeature);
    locFeatures.push(TUPPfeature);
    locFeatures.push(WFMBfeature);

    var vectorSource = new ol.source.Vector({
        features: locFeatures //add an array of features
    });

    var iconStyle = new ol.style.Style({
         image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
         anchor: [0.5, 0.5],
         opacity: 0.75,
         src: 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
        }))
    });
    
    var locVectorLay = new ol.layer.Vector({
        source: vectorSource,
        style: iconStyle
    });

    var selemap = new ol.Map({
        layers: [sBase, locVectorLay],
     target: 'selemap',
     view: sview
    });


