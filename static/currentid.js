$(document).ready(function () {
  $("#detialss").hide();
  var lst_data = "";
  function quote() {
    $.getJSON("https://api.quotable.io/random", function (data) {
      $("#something").html(
        "<q id='justi'><b>" +
          data["content"] +
          "</q>-- <q>" +
          data["author"] +
          "</b></q>"
      );
    });
  }
  quote();
  setInterval(() => {
    $.getJSON("/c_id", function (data) {
      if (JSON.stringify(data) === "{}") {
        $("#detialss").hide();
      } else if (JSON.stringify(lst_data) !== JSON.stringify(data)) {
        lst_data = data;
        let colour = data["status"] == "IN" ? "lightgreen" : "red";
        $("#idcard").removeClass("bg-dark");
        $("#idcard").addClass("bg-warning");
        content =
          "<br><b>AD No:  " +
          data["adno"] +
          "<br><br>Name:  " +
          data["name"] +
          "<br><br>Batch: " +
          data["batch"] +
          "<br><br>Time:  " +
          data["time"] +
          "<br><br><span style=':50px;border-radius: 10px;background-color: " +
          colour +
          "'>&nbsp;&nbsp;Status: " +
          data["status"] +
          "&nbsp;&nbsp;</span></b>";
        $("#detials").html(content);
        $("#detialss").show();
        $("#qr").hide();
        quote();

        setTimeout(() => {
          $("#idcard").removeClass("bg-warning");
          $("#idcard").addClass("bg-dark");
          $("#detialss").hide();
          $("#qr").show();
        }, 3000);
      }
    });
  }, 2000);
});
