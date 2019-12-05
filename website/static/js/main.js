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
        var prediction = "<h1>" + JSON.stringify(json_response.result.predicted).replace(/[#_.\"]|train|test|csv/g, "") + "</h1>";
        var predicted_sheets = "";
        var sheet_info = "";
        for(index in json_response.result.top_five){
          sheet_names = json_response.result.top_five[index]
          var sheet_name = JSON.stringify(sheet_names.name).replace(/[#_.\"]|train|test|csv/g, "");
          predicted_sheets += "<a class=\"list-group-item list-group-item-action\" id=\"list-{}-list\" data-toggle=\"list\" href=\"#list-{}\" role=\"tab\" aria-controls=\"{}\">{}</a>".format(sheet_name, sheet_name, sheet_name, sheet_name)
          sheet_info += `<div class="tab-pane fade" id="list-`+sheet_name+`" role="tabpanel" aria-labelledby="list-`+sheet_name+`-list"><table><tr><th>`+sheet_name+`</th></tr><tr><td>hamming distance : </td><td>`+sheet_names.hamming+`</td></tr></table></div>`
        }
        $('#list-tab').html(predicted_sheets);
        $('#nav-tabContent').html(sheet_info);
        $('#top-result').html(prediction.toUpperCase());
        $('#input-sheet').html("<p>Input sheet: {}</p>".format(JSON.stringify(json_response.result.input_fingerprint).replace(/[\"]/g, "")))
        $('#more-information').html("<p>More information:</p>")
        $('#list-tab a:first-child').tab('show')
      });
    });
  });