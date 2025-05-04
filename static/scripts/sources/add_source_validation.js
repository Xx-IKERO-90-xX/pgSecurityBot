const regex = /^https?:\/\/[^\s]+\.txt(?:\?[^\s]*)?(?:#[^\s]*)?$/i;

let form_source = document.getElementById('form_add_source');
let alert_div = document.getElementById("alerts_div");

function loadPage() {
    alert_div.innerHTML = "";
}

form_source.addEventListener("submit", (event)=> {
    let new_source = document.getElementById("new_source_input").value;

    let errorTemplate = document.getElementById("sourceErrorAlertTemplate").content.cloneNode(true);
    let errorAlert = errorTemplate.getElementById("sourceErrorAlert");

    if (!regex.test(new_source)){
        alert_div.innerHTML = "";
        alert_div.append(errorAlert);
        event.preventDefault();
    }
});