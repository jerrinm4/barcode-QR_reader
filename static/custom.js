//create document ready function
$(document).ready(function(){

//create function to display the time
	function displayTime(){
//create variable currentTime and have the Date() object store computer's time
		var currentTime = new Date();
//create variables for hours, minutes, and seconds		
		var hours = currentTime.getHours();
		var minutes = currentTime.getMinutes();
		var seconds = currentTime.getSeconds();	
		var meridiem = " AM";

		if(hours>11){
			hours = hours - 12;
			meridiem = " PM";
		}
		if(hours === 0){
			hours = 12;
		}
		if (hours<10){
			hours = "0" + hours;
		}
		if (minutes<10){
			minutes = "0" + minutes;
		}
		if (seconds<10){
			seconds = "0" + seconds;
		}
		$("#clock").text(hours + ":" + minutes + ":" + seconds +  meridiem);
		//set variable to change clockDiv in HTML
		//var clockDiv = document.getElementById('clock');

		//innerText to set text inside an HTML element
		//clockDiv.innerText = hours + ":" + minutes + ":" + seconds + meridiem;
	}
	function displayDay(){
		var currentDay = new Date();
		var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
		var day = days[currentDay.getDay()];
		$("#day").text(day);
	}	
	function displayDate(){
		var currentDate = new Date();
		var year = currentDate.getFullYear();
		var date = currentDate.getDate();
		var months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
		var month = months[currentDate.getMonth()];
		if (date<10){
			date = "0" + date;
		}

		$("#date").text(month +" "+ date +" "+ year);
	}
	displayTime();
	setInterval(displayTime, 1000);
	displayDay();
	displayDate();

});