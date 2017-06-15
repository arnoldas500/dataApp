

var $l1opacity = $('#l1-opacity');
var $l2opacity = $('#l2-opacity');

$('#l1-slider').slider({
    min: 0,
    max: 100,
    value: 100,
    slide: function(event, ui) {
        $l1opacity.text(ui.value + '%');
        dispmap.getLayers().item(1).setOpacity(ui.value / 100);
    }
});

$('#l2-slider').slider({

    min: 0,
    max: 100,
    value: 100,
    slide: function(event, ui) {
        $l2opacity.text(ui.value + '%');
        dispmap.getLayers().item(2).setOpacity(ui.value / 100);
    }
});