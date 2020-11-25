function student_display(){
  //toggle with the visibility
  var stuList = document.querySelectorAll('.studentInfo');
  var empList = document.querySelectorAll('.employeeInfo');
  for (var x = 0; x < stuList.length; x++ ) {
    stuList[x].style.visibility="visible";
  }

  for (var y = 0; y < empList.length; y++ ) {
    empList[y].style.visibility="hidden";
  }

  //set the input value
  document.getElementsByName("Type").values()[0] = "student" ;

  $('#Location').required = "true";
  $('#HouseType').required = "true";




  //clear the employee value
  var jobs = document.getElementsByName("employType")
  for (var i=0;i<jobs.length;i++) {
    jobs[i].checked = false;
  }
  document.getElementById("Phone").value = "";
  $('#Role').required = "false";
  $('#Phone').required = "false";



}

function employee_display(){
  var stuList = document.querySelectorAll('.studentInfo');
  var empList = document.querySelectorAll('.employeeInfo');
  for (var x = 0; x < stuList.length; x++ ) {
    stuList[x].style.visibility="hidden";
  }

  for (var x = 0; x < empList.length; x++ ) {
    empList[x].style.visibility="visible";
  }

  document.getElementsByName("Type").values()[0] = "employee" ;
  $('#Role').required = "true";
  $('#Phone').required = "true";
  $('#Location').required = "false";
  $('#HouseType').required = "false";

  //clear the student value:
  document.getElementById("Location").value = "";
  document.getElementById("HouseType").value = "";





}
