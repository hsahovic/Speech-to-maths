function accountAjax (formID) {
    $.ajax({
        headers: {
            "X-CSRFToken" : document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        type: "POST",
        url: links[formID],
        data: $("form#" + formID).serialize(),
        dataType : "json",
        success: function(json) {
            communicationIndicatorManager.endRequest();
            switch (json.action) {
                case "updateForm" :
                    document.getElementById(formID).getElementsByTagName("table")[0].innerHTML = json.html;
                    break;
                case "informSuccess" :
                    document.getElementById(formID).innerHTML = successMessage[formID];
                    fillViewport();
                    break;
                case "redirect" :
                    window.location.replace(json.newAdress);
            }               
        }
    });
    communicationIndicatorManager.addRequest();
}
