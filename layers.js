
        
    var vLay1, vLay2;
        
    function pad(d) {
        return (d < 10) ? '0' + d.toString() : d.toString();
    }
    
   function updateDisplayMap(loc, hr) {
        var numDispLays = dispmap.getLayers().getLength();
        var ctrlpane = document.getElementById('pane');
        ctrlpane.style.visibility="visible";

        if (numDispLays > 1) {
            dispmap.removeLayer(vLay1);
            dispmap.removeLayer(vLay2);
        }
        
        // Now add the 2 new layers to the display map

        var lay1src = loc + "_" + hr + "_00000_00150.kml";
        var lay2src = loc + "_" + hr + "_00150_00300.kml";

        var l1url = "model/data/kml_" + loc + "/" + lay1src;
        $.ajax(l1url).then(function(kmlresponse) {
            var kmlFormat = new ol.format.KML();
            var l1pmark = kmlFormat.readFeature(kmlresponse);
            var l1legend = "model/data/kml_" + loc + "/" + l1pmark.get('name');
            $("#legend1").attr("src", l1legend);
        });
        
        vLay1 = new ol.layer.Vector({
            source: new ol.source.Vector({
                format: new ol.format.KML(),
                url: "model/data/kml_" + loc + "/" + lay1src
            })
        });
                
        var l2url = "model/data/kml_" + loc + "/" + lay2src;
        $.ajax(l2url).then(function(kmlresponse) {
            var kmlFormat = new ol.format.KML();
            var l2pmark = kmlFormat.readFeature(kmlresponse);
            var l2legend = "model/data/kml_" + loc + "/" + l2pmark.get('name');
            $("#legend2").attr("src", l2legend);
        });
        
        
        vLay2 = new ol.layer.Vector({
            source: new ol.source.Vector({
                format: new ol.format.KML(),
                url: "model/data/kml_" + loc + "/" + lay2src
            })
        });
        
        dispmap.addLayer(vLay1);
        dispmap.addLayer(vLay2);
    }

//    var hrchng = document.querySelector('#simhr');
//    hrchng.addEventListener('change', function() {
//        alert("Hour: "+document.getElementById('simhr').value); 
//    });

    function spyderRun(){
//    stuff from the other file


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

        var BELLfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-76.11765, 43.78823],
            'EPSG:4326', 'EPSG:3857')),
            name: 'BELL'
        });

        var BUFFfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-78.76717, 43.00017],
                    'EPSG:4326','EPSG:3857')),
            name: 'BUFF'
        });

        var CESTMfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.832332, 42.692142],
                    'EPSG:4326','EPSG:3857')),
            name: 'CESTM_roof-14'
        });

        var CHAZfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.46634, 44.889],
                    'EPSG:4326','EPSG:3857')),
            name: 'CHAZ'
        });

        var CLYMfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-79.62746, 42.02143],
                    'EPSG:4326','EPSG:3857')),
            name: 'CLYM'
        });

        var EHAMfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-72.20094, 40.970394],
                    'EPSG:4326','EPSG:3857')),
            name: 'EHAM'
        });

        var JORDfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-76.469993, 43.068747],
                    'EPSG:4326','EPSG:3857')),
            name: 'JORD'
        });

        var OWEGfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-76.253072, 42.024938],
                    'EPSG:4326','EPSG:3857')),
            name: 'OWEG'
        });

        var QUEEfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.815856, 40.734335],
                    'EPSG:4326','EPSG:3857')),
            name: 'QUEE'
        });

        var REDHfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.88412, 41.99983],
                    'EPSG:4326','EPSG:3857')),
            name: 'REDH'
        });

        var VOORfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.97562, 42.65242],
                    'EPSG:4326','EPSG:3857')),
            name: 'VOOR'
        });

        var SUFFfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-74.085979, 41.133034],
                    'EPSG:4326','EPSG:3857')),
            name: 'SUFF'
        });

        var TUPPfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-74.43826, 44.22128],
                    'EPSG:4326','EPSG:3857')),
            name: 'TUPP'
        });

        var WANTfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.5054, 40.65025],
                    'EPSG:4326','EPSG:3857')),
            name: 'WANT'
        });

        var WFMBfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-73.858829, 44.393236],
                    'EPSG:4326','EPSG:3857')),
            name: 'WFMB'
        });

        var WEBSfeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([-77.41238, 43.2601],
                    'EPSG:4326','EPSG:3857')),
            name: 'WEBS'
        });

        locFeatures.push(BELLfeature);
        locFeatures.push(BUFFfeature);
        locFeatures.push(CHAZfeature);
        locFeatures.push(CLYMfeature);
        locFeatures.push(CESTMfeature);
        locFeatures.push(EHAMfeature);
        locFeatures.push(JORDfeature);
        locFeatures.push(OWEGfeature);
        locFeatures.push(QUEEfeature);
        locFeatures.push(REDHfeature);
        locFeatures.push(VOORfeature);
        locFeatures.push(SUFFfeature);
        locFeatures.push(TUPPfeature);
        locFeatures.push(WANTfeature);
        locFeatures.push(WEBSfeature);
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


        /**
         * Elements that make up the popup
         */
        var container = document.getElementById('popup');
        var content = document.getElementById('popup-content')
        var closer = document.getElementById('popup-closer');

        //content.onclick = function() {inputChange()};
        /*
        container.onclick = function() {inputChange()};

        //drop down for onclick
        function inputChange(){
        //document.getElementById("myDropDown").classList.toggle("show");
        var selectBox = document.getElementById("state2");
        var selectedValue = selectBox.options[selectBox.selectedIndex].value;
        alert(selectedValue);
        alert(selectBox);
        if(selectBox != selectedValue){
        selectBox.options[selectBox.selectedIndex].value = "CESTM_roof-14"}
        alert(selectBox.options[selectBox.selectedIndex].value);
        selectBox.options[selectBox.selectedIndex].dispatchEvent(new Event('change'));
        };
*/
        /**
         * Add a click handler to hide the popup.
         * @return {boolean} Don't follow the href.
         */
        if(closer === null)
         {return;}
        closer.onclick = function() {
            poplay.setPosition(undefined);
            closer.blur();
            return false;
        };

        var poplay = new ol.Overlay({
            element: container,
            autoPan: true
        });

        selemap.addOverlay(poplay);

        // display popup on click
        selemap.on('click', function(evt) {
            var feature = selemap.forEachFeatureAtPixel(evt.pixel,
                function(feature) {
                //selecting the correct graphs to show based to the site selected
                    var selectBox = document.getElementById("state2");
                var selectedValue = selectBox.options[selectBox.selectedIndex].value;
                //alert(selectedValue);
                //alert(selectBox);
                if(selectBox != selectedValue){
                selectBox.options[selectBox.selectedIndex].value = feature.get('name')}
                alert(selectBox.options[selectBox.selectedIndex].value);
                selectBox.options[selectBox.selectedIndex].dispatchEvent(new Event('change'));
                    return feature;
            });

            if (feature) {
              var coordinates = feature.getGeometry().getCoordinates();
              var locName = feature.get('name');
              content.innerHTML = locName;
              poplay.setPosition(coordinates);

              var simHour = pad(document.getElementById('simhr').value);

              updateDisplayMap(locName, simHour);

              //selecting the correct graphs to show based to the site selected
                var selectBox = document.getElementById("state2");
                var selectedValue = selectBox.options[selectBox.selectedIndex].value;
                alert(selectedValue);
                alert(selectBox);
                if(selectBox != selectedValue){
                selectBox.options[selectBox.selectedIndex].value = locName}
                alert(selectBox.options[selectBox.selectedIndex].value);
                selectBox.options[selectBox.selectedIndex].dispatchEvent(new Event('change'));
            }
        });

        var target = selemap.getTarget();
        var jTarget = typeof target === "string" ? $("#" + target) : $(target);
        // change mouse cursor when over marker
        $(selemap.getViewport()).on('mousemove', function (e) {
            var pixel = selemap.getEventPixel(e.originalEvent);
            var hit = selemap.forEachFeatureAtPixel(pixel, function (feature, layer) {
               return true;
            });
            if (hit) {
               jTarget.css("cursor", "pointer");
            } else {
               jTarget.css("cursor", "");
            }
        });
    }

  
