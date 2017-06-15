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
        var l1legend;
        $.ajax(l1url).then(function(kmlresponse) {
            var kmlFormat = new ol.format.KML();
            var l1pmark = kmlFormat.readFeature(kmlresponse);
            l1legend = "model/data/kml_" + loc + "/" + l1pmark.get('name');
        });
        
        $("#legend1").attr("src", l1legend);
        
        vLay1 = new ol.layer.Vector({
            source: new ol.source.Vector({
                format: new ol.format.KML(),
                url: "model/data/kml_" + loc + "/" + lay1src
            })
        });
                
        var l2url = "model/data/kml_" + loc + "/" + lay2src;
        var l2legend;
        $.ajax(l2url).then(function(kmlresponse) {
            var kmlFormat = new ol.format.KML();
            var l2pmark = kmlFormat.readFeature(kmlresponse);
            l2legend = "model/data/kml_" + loc + "/" + l2pmark.get('name');
        });
        
        $("#legend2").attr("src", l2legend);
        
        vLay2 = new ol.layer.Vector({
            source: new ol.source.Vector({
                format: new ol.format.KML(),
                url: "model/data/kml_" + loc + "/" + lay2src
            })
        });
        
        dispmap.addLayer(vLay1);
        dispmap.addLayer(vLay2);
    }
