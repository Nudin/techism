$(function() {
    $.datepicker.setDefaults($.datepicker.regional["de"]);
    $("#id_date_time_begin_0").datepicker($.datepicker.regional["de"]);
    $("#id_date_time_end_0").datepicker($.datepicker.regional["de"]);

    // load locations via AJAX, add 'label' for auto completion
    var availableLocs = [];
    $.getJSON("/events/locations/", {
        ajax : 'true'
    }, function(jsonLocation) {
        jsonLocation.map(function(item) {
            item.label = item.name + ', ' + item.street + ', ' + item.city;
            availableLocs.push(item);
        });
    });

    // activate auto completion for location
    $("#id_location_name").autocomplete({
        source : availableLocs,
        select : function(event, ui) {
            $("#id_location_name").val(ui.item.name);
            $("#id_location_street").val(ui.item.street);
            $("#id_location_city").val(ui.item.city);
            $("#id_location_latitude").val(ui.item.latitude);
            $("#id_location_longitude").val(ui.item.longitude);
            $("#id_location").val(ui.item.id);
            map.displayLatLon(ui.item.latitude, ui.item.longitude);
            return false;
        }
    });

    // initialize the map
    var map = new Techism.Map.Map(function(lat, lon) {
        $("#id_location_latitude").val(lat);
        $("#id_location_longitude").val(lon);
    });

    // display location if one is given
    var latitude = $("#id_location_latitude").val();
    var longitude = $("#id_location_longitude").val();
    if (latitude && longitude) {
        map.displayLatLon(latitude, longitude);
    }

    // show coordinates in map when button is clicked
    $("#id_location_show_in_map").click(function() {
        var street = $("#id_location_street").val();
        var city = $("#id_location_city").val();
        map.displayLocation(street, city);
    });
});