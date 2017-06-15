
        
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
    
    /**
     * Elements that make up the popup
     */
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');
    
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
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
                return feature;
        });
        
        if (feature) {
          var coordinates = feature.getGeometry().getCoordinates();
          var locName = feature.get('name');
          content.innerHTML = locName;
          poplay.setPosition(coordinates);
          
          var simHour = pad(document.getElementById('simhr').value);
           
          updateDisplayMap(locName, simHour);
          
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
    

  
