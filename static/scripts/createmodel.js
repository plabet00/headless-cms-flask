function PopupMenu() {
  $("#body").append("<div id = 'popup' class = 'popup_style'></div>");
  let form = $(
    "<form method = 'get' ><input type = 'text' name = 'name'><br><input type = 'submit' value = 'Submit'><form>"
  );
  $("#popup").append(form);
  let dimmer = $("<div id = 'dimmer' class = 'dimmer' ></div>");
  $("body").append(dimmer);
}
