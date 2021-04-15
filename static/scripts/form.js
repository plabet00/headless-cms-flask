let state = [];
let counter = 0;
function PopupForm() {
  $("#body").append("<div id = 'popup' class = 'popup_style'></div>");

  let listOfItems = ["text", "image", "number"];
  for (x in listOfItems) {
    var button = $(
      "<button>" +
        listOfItems[x].charAt(0).toUpperCase() +
        listOfItems[x].slice(1) +
        "</button>"
    ).click(function () {
      FormAddOnClick($(this)[0].innerHTML);
    });
    $("#popup").append(
      "<img src = 'static/images/" +
        listOfItems[x] +
        ".png' height = 20 width = 20>"
    );
    $("#popup").append(button);
  }
  $("#popup").append("<br>");
  let cancelButton = $("<button>Cancel</button>").click(ClosePopup);
  $("#popup").append(cancelButton);
  let dimmer = document.createElement("div");
  dimmer.id = "dimmer";
  popup.className = "popup_style";
  dimmer.className = "dimmer";
  document.getElementById("body").appendChild(popup);
  document.getElementById("body").appendChild(dimmer);
}

function ClosePopup() {
  document.getElementById("popup").remove();
  document.getElementById("dimmer").remove();
}

function FormAddOnClick(formType) {
  document.getElementById("popup").remove();
  let popup = $("<div class = 'popup_style' id = 'popup'></div>");
  $("#body").append(popup);
  let message = $("<div>Type in the name of your " + formType + " field</div>");
  let input = $(
    "<form id = 'form1'><input type='text' name = 'text'><input type='submit' value = 'Submit'></form>"
  ).submit(function (e) {
    e.preventDefault();
    SubmitForm(formType);
  });
  $("#popup").append(message);
  $("#popup").append("<br>");
  $("#popup").append(input);
  $("#popup").append("<br>");
  let cancelButton = $("<button>Cancel</button>").click(ClosePopup);
  $("#popup").append(cancelButton);
}

function SubmitForm(formType) {
  if ($("#form1").serializeArray()[0].value !== "") {
    state.push({ name: $("#form1").serializeArray()[0].value, type: formType });
    let addedForm = $(
      "<input value = " +
        $("#form1").serializeArray()[0].value +
        " name = " +
        formType + counter +
        " type = 'hidden'>" +
        "<br>"
    );
    counter += 1;
    ClosePopup();
    addedForm.insertBefore("#button_style")
  } else {
  }
}
