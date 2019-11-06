$(document).ready(function(){
    $('form input').change(function () {
      $('form p').text(this.files[0].name);
    });

    String.prototype.format = function () {
      var i = 0, args = arguments;
      return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
      });
    };

    $("#run-query").click(function(e) {
      console.log("QUERY RUNNING")
      e.preventDefault();
      var form = new FormData();    
      form.append("file", jQuery('#file')[0].files[0]);
          
      var settings = {
        "async": true,
        "crossDomain": true,
        "url": backendURL+"/api/analyze",
        "method": "POST",
        "processData": false,
        "contentType": false,
        "mimeType": "multipart/form-data",
        "data": form
      }
      
      $.ajax(settings).done(function (response) {
        json_response = JSON.parse(response);
        var prediction = "<h1>" + JSON.stringify(json_response.prediction).replace(/[#_.\"]|train|test|csv/g, "") + "</h1>";
        var predicted_sheets = "";
        var sheet_info = "";
        for(sheet_names in json_response.predicted_sheets)
        {
          var sheet_name = JSON.stringify(sheet_names).replace(/[#_.\"]|train|test|csv/g, "")
          var cosine_score = json_response.predicted_sheets[sheet_names].cosine_similarity_score;
          var avgMoe = json_response.predicted_sheets[sheet_names].avgMoe;
          var avgSg = json_response.predicted_sheets[sheet_names].avgSg;
          var avgMc = json_response.predicted_sheets[sheet_names].avgMc;
          var avgVel = json_response.predicted_sheets[sheet_names].avgVel;
          var avgUPT = json_response.predicted_sheets[sheet_names].avgUPT;
          var pkDensity = json_response.predicted_sheets[sheet_names].pkDensity;
          predicted_sheets += "<a class=\"list-group-item list-group-item-action\" id=\"list-{}-list\" data-toggle=\"list\" href=\"#list-{}\" role=\"tab\" aria-controls=\"{}\">{}</a>".format(sheet_name, sheet_name, sheet_name, sheet_name)
          sheet_info += "<div class=\"tab-pane fade\" id=\"list-{}\" role=\"tabpanel\" aria-labelledby=\"list-{}-list\">\
                          <table>\
                            <tr><th>{}</th></tr>\
                            <tr><td>cosine score : </td><td>{}</td></tr>\
                            <tr><td>avgMoe       : </td><td>{}</td></tr>\
                            <tr><td>avgSg        : </td><td>{}</td></tr>\
                            <tr><td>avgMc        : </td><td>{}</td></tr>\
                            <tr><td>avgVel       : </td><td>{}</td></tr>\
                            <tr><td>avgUPT       : </td><td>{}</td></tr>\
                            <tr><td>pkDensity    : </td><td>{}</td></tr>\
                          </table>\
                        </div>".format(sheet_name, sheet_name, sheet_name, cosine_score, avgMoe, avgSg, avgMc, avgVel, avgUPT, pkDensity)
        }
        $('#list-tab').html(predicted_sheets);
        $('#nav-tabContent').html(sheet_info);
        $('#top-result').html(prediction.toUpperCase());
        $('#input-sheet').html("<p>Input sheet: {}</p>".format(JSON.stringify(json_response.input_sheet).replace(/[\"]/g, "")))
        $('#more-information').html("<p>More information:</p>")
        $('#list-tab a:first-child').tab('show')
      });
    });
  });
