/*!
 * ARC.js
 *
 * Copyright 2013-2014, Gary Dalton
 */

/* Document actions
----------------------------------*/
$(document).ready(function() {
    $( "#myradio" ).buttonset();
    
  // WIZARD CODE
  if ($('#wizard').length){
  
    // Validation
    jQuery.validator.addMethod("phoneUS", function(phone_number, element) {
        phone_number = phone_number.replace(/\s+/g, ""); 
      return this.optional(element) || phone_number.length > 9 &&
        phone_number.match(/^(1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
    }, "Please specify a valid phone number");
    var validator = $("#IntakeIncidentWizardForm").validate({
      //debug: true,
      //onsubmit: true,
      //errorContainer: "#messageBox1",
      //errorLabelContainer: "#messageBox1 ul",
      //wrapper: "li",
      rules: {
        // STEP 1: THE CALL
        "data[IntakeCall][call_datetime]": {
          required: true,
        },
        "data[IntakeCall][caller]": {
          required: true,
          minlength: 2,
        },
        "data[IntakeCall][callback_number]": {
          required: true,
          phoneUS: true,
        },
        "data[IntakeCall][caller_agency]": {
          required: true,
          minlength: 2,
        },
        // STEP 2: INCIDENT NAME
        "data[IntakeIncident][incident_name]": {
          required: true,
        },
        "data[IntakeIncident][start_datetime]": {
          required: true,
          minlength: 2,
        },
        "data[IntakeIncident][street_address]": {
          required: true,
          minlength: 5,
        },
        "data[IntakeIncident][city_zip]": {
          required: true,
          minlength: 2,
        },
        "data[IntakeIncident][state]": {
          required: true,
          minlength: 2,
        },
        "data[IntakeIncident][city]": {
          required: true,
          minlength: 2,
        },
        "data[IntakeIncident][zip_code]": {
          required: true,
          minlength: 5,
        },        
      },
      highlight: function(label) {
          $(label).closest('.control-group').addClass('error');
      },
      success: function(label) {
          label
          .text('OK!').addClass('valid')
          .closest('.control-group').addClass('success');
      }

    });
    // end Validation
  
    loadScript();
    var sisyphus = $('form').sisyphus({timeout: 10});
    $('#IntakeCallCallDatetime').datetimepicker({
      ampm: true,
      stepMinute: 5,
    });
    $('#IntakeIncidentStartDatetime').datetimepicker({
      ampm: true,
      stepMinute: 5,
    });
    
    // Incident naming help
    var $incidentnamehelp = $('<div></div>')
      .html('<p><img src="https://secure.npexchange.org/libs/ggis/img/icon-help.png"  height="20" width="20"> <b>Incident Naming Help</b></p><p>Use the address verification and incident naming generator whenever possible. Occassionally, it may be neccessary to use the bypass.</p><p>Incidents are named according to a pattern. Please try to follow the pattern as described.</p><p>County State Month/Year StreetName StreetDirection</p><p>As an example, an incident at 2123 W Scott St, Milwaukee, WI 53204, USA, on August 6, 2012 would be named:</p><p>Milwaukee WI 08/12 Scott St W</p>')
      .dialog({
        autoOpen: false,
        title: 'Incident Naming'
		});
    $("#incidentnamehelp").click(function(){
      $incidentnamehelp.dialog('open');
      return false;
    });
    // Incident naming warning
    var $incidentnamewarning = $('<div></div>')
      .html('<p><img src="https://secure.npexchange.org/libs/ggis/img/icon-warn.png"  height="20" width="20"> <b>Incident Name Warning</b></p><p>Use the address verification and incident naming generator whenever possible.</p>')
      .dialog({
        autoOpen: false,
        title: 'Incident Name Warning'
		});
    // Generator Switching
    $("#turn-generator-on").click(function(){
      $("#turn-generator-on").addClass("btn-success");
      $("#turn-generator-on").text('ON');
      $("#turn-generator-off").removeClass("btn-danger");
      $("#turn-generator-off").text('Turn Off');
      $("#IntakeIncidentCityZip").removeAttr("disabled");
      
      $("#IntakeIncidentIncidentName").attr('disabled', 'disabled');
      $("#IntakeIncidentCity").attr('disabled', 'disabled');
      $("#IntakeIncidentZipCode").attr('disabled', 'disabled');
      $("#IntakeIncidentCounty").attr('disabled', 'disabled');
      $("#IntakeIncidentLatitude").attr('disabled', 'disabled');
      $("#IntakeIncidentLongitude").attr('disabled', 'disabled');
      $("#span_IntakeIncidentIncidentName").removeClass('required');
      $("#span_IntakeIncidentCityZip").addClass('required');
      $("#span_IntakeIncidentCity").removeClass('required');
      $("#span_IntakeIncidentZip").removeClass('required');
      
      return false;
    });
    $("#turn-generator-off").click(function(){
      $("#span_IntakeIncidentCity").addClass('required');
      $("#turn-generator-on").removeClass("btn-success");
      $("#turn-generator-on").text('Turn On');
      $("#turn-generator-off").addClass("btn-danger");
      $("#turn-generator-off").text('OFF');
      $("#IntakeIncidentCityZip").attr('disabled', 'disabled');
      $("#IntakeIncidentIncidentName").removeAttr("disabled");
      $("#IntakeIncidentCity").removeAttr("disabled");
      $("#IntakeIncidentZipCode").removeAttr("disabled");
      $("#IntakeIncidentCounty").removeAttr("disabled");
      $("#IntakeIncidentLatitude").removeAttr("disabled");
      $("#IntakeIncidentLongitude").removeAttr("disabled");
      $("#span_IntakeIncidentIncidentName").addClass('required');
      $("#span_IntakeIncidentCityZip").removeClass('required');
      $("#span_IntakeIncidentZip").addClass('required');
      $incidentnamewarning.dialog('open');
      return false;
    });
    
    // Step 1 CLICKED
    $("#btn-go-step-2").click(function() {
      if (tab_validate("input.tab0")){
        $('#wizard').tabs("enable", 1);
        $('#wizard').tabs("select", 1);
        resizeMap(map);
      }
    });
    // Step Address Validate CLICKED
    $("#btn-address-validate").click(function() {

      if ( $("#turn-generator-on").hasClass("btn-success") ){
        var valid = true;
        if (!$("#IntakeIncidentWizardForm").validate().element("#IntakeIncidentStartDatetime") && valid) {
              valid = false;
        }
        if (!$("#IntakeIncidentWizardForm").validate().element("#IntakeIncidentStreetAddress") && valid) {
              valid = false;
        }
        if (!$("#IntakeIncidentWizardForm").validate().element("#IntakeIncidentCityZip") && valid) {
              valid = false;
        }
        if (!$("#IntakeIncidentWizardForm").validate().element("#IntakeIncidentState") && valid) {
              valid = false;
        } 
      }
      if ( valid ){
        console.log("Time to generate");
      }
      
      // Begin address checking
      checkAddress();
    
        
    });
    
    // Clear Local Storage (to reset form)
    $("#btn-clear-sisyphus").click(function() {
        sisyphus.manuallyReleaseData();
    });
    
    
    // Step 2 CLICKED
    $("#btn-go-step-3").click(function() {
      if (tab_validate("input.tab1")){
        $('#wizard').tabs("enable", 1);
        $('#wizard').tabs("select", 1);
        resizeMap(map);
      }
    });
    
    
    function tab_validate(index){
      var valid = true;
      var $inputs = $("#wizard").find(index);
      $inputs.each(function() {
        console.log(this);
          if (!$("#IntakeIncidentWizardForm").validate().element(this) && valid) {
              valid = false;
          }
      });
      return valid;
    }

    
    
  }
  // end WIZARD CODE

});



/* Page Setup function
----------------------------------*/
function page_setup(myform){
  if ( myform == "EmailListIndexForm" ){
    $('.ggis_hide').hide();
  }
}

function toggle_hours(){
  if ( $('input[name="data[Temp][frequency]"]:checked', '#EmailListIndexForm').val() == "Selected" ){
    $('.ggis_hide').show();
  }else{
    $('.ggis_hide').hide();
  }
}

/* Utility functions
----------------------------------*/
function lpad(originalstr, length, strToPad) {
  while (originalstr.length < length)
    originalstr = strToPad + originalstr;
  return originalstr;
}
function rpad(originalstr, length, strToPad) {
  while (originalstr.length < length)
    originalstr = originalstr + strToPad;
  return originalstr;
}

/* Incident Naming functions
----------------------------------*/
function buildIncidentName(address_components){
    // 04/10/14 23:15 - WAUKESHA, BROOKFIELD (1234 S 100th ST) – MFF 4-8 – IND ASSIST, CANTEENING - BOB WADE 414-412-5412
  var directionals = ["N", "S", "E", "W", "NW", "NE", "SW", "SE"];
  var routeArray = address_components["route"].split(/ /);
  var dateArray = $("#IntakeIncidentStartDatetime").val().split("/");
  var newString;
  var compasspoint = false;
  var county = address_components["administrative_area_level_2"];
  
  console.log(dateArray);
  // alert(routeArray[0].length);
  if (routeArray[0].length < 3){
    $.each( directionals, function(idx, direction){
      if (routeArray[0] == direction){
        compasspoint = direction;
        return false;
      }
    });
  }
  
  county = county.replace(" County", "");
  county = county.toUpperCase();
  newString = $("#IntakeIncidentStartDatetime").val() + " - " + county + ", " + address_components["locality"];
  newString = newString + " (" + $.trim(address_components["street_number"]) + " " + $.trim(address_components["route"]) + ") ";
  // newString = address_components["locality"] + " " + address_components["administrative_area_level_1"] + " " + dateArray[0] + "/" + dateArray[2].slice(2);
  if ( compasspoint.length ) {
     // newString = newString + " (" + $.trim(address_components["street_number"]) + " " + $.trim(address_components["route"]) + ") ";
    //newString = newString + " " + compasspoint + " " + $.trim(address_components["route"].slice(routeArray[0].length));
  }else{
    //newString = newString + " " + $.trim(address_components["route"]);
  }
  return newString;
}

/* Google Mapping functions
----------------------------------*/
var map;
var geocoder;
var results;

function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyB_XgZo0ZU1fm3JJeaGk3qtaAUzbp8jYFY&sensor=false&callback=initialize";
  document.body.appendChild(script);
}
function initialize() {
  geocoder = new google.maps.Geocoder();
  var myOptions = {
    center: new google.maps.LatLng(43.8, -87.9),
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}
function buildGoogleMapUrl(fulladdress){
  var mapurl = "http://maps.google.com/maps?hl=en";
  var zoom = 12;
  var encodeaddress = fulladdress.replace(" ", "+");
  mapurl = mapurl + 
          //"&ll=" + lat +
          //"," + lon +
          "&q=" + encodeaddress +
          "&z=" + zoom;
  return mapurl;
}
function resizeMap(m) {
    x = m.getZoom();
    c = m.getCenter();
    google.maps.event.trigger(m, 'resize');
    m.setZoom(x);
    m.setCenter(c);
};

function catchGeoData(address){
  codeAddress(address, function(results){
    var isstreetaddress = false;
    $.each(results.types,  function(idx, value){
      if (value == "street_address"){
        isstreetaddress = true;
      }
    });
    //formatted_address = addr;
    //alert(addr);
    //traverse(results.address_components, process);
    //alert(results.formatted_address);
    //alert(results.types);
    //alert(results.geometry.location.toString());
    //alert(results.geometry.location.lng());
    //alert(results['route']);
    if(isstreetaddress){
      var wantedtypes = ["street_number", "route", "locality", "administrative_area_level_1", "administrative_area_level_2", "postal_code"];
      $.each( wantedtypes, function(ctr, wanted){
        $.each(results.address_components, function(index, value) {
          //alert(index + ': ' + value);
          $.each(value.types, function(idx, val){
            if (val == wanted){
              //alert(idx + ': ' + val);
              //alert(index + ': ' + value.long_name);
              results[wanted] = value.short_name;
            }
          });
        });
      });
      
      var incidentname = buildIncidentName(results);
      console.log(incidentname);
      // SET FIELD VALUES
      $("#IntakeIncidentIncidentName").val(incidentname);
      $("#IntakeIncidentCounty").val(results["administrative_area_level_2"]);
      $("#IntakeIncidentZipCode").val(results["postal_code"]);
      $("#IntakeIncidentCity").val(results["locality"]);
      $("#IntakeIncidentLatitude").val(results.geometry.location.lat());
      $("#IntakeIncidentLongitude").val(results.geometry.location.lng());
      $( "#messageBox2" ).append(results.formatted_address);
      $("#IntakeIncidentStreetAddress").val(results["street_number"] + " " + results["route"] );
      // SET MAP ZOOM AND LINK
      map.setZoom(12);
      mapurl = buildGoogleMapUrl(results.formatted_address);
      //mapurl = buildGoogleMapUrl(results.geometry.location.lat(), results.geometry.location.lng());
      $('a.replaceme').replaceWith('<a href="' + mapurl + '"  class="replaceme">Map in Google</a>');
      
    }else{
      alert("Not a valid street address. Please try again");
    }
  });
}
      
function codeAddress(address, callback) {
    console.log(callback);
  //var address = document.getElementById("address").value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
      callback(results[0]);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
      
function checkAddress(){
    //$( "#messageBox2" ).show();
    address = $("#IntakeIncidentStreetAddress").val() + ', ' +
            $("#IntakeIncidentCityZip").val() + ', ' +
            $("#IntakeIncidentState").val();
    console.log(address);
    catchGeoData(address);
    console.log(address);
    //codeAddress(address, map);
    
    //$( "#messageBox2" ).append(appendtext);
}
