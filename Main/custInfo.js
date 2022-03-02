//listen for submit event//
document.getElementById('waitListForm').addEventListener('submit', formSubmit);

//Submit form//
function formSubmit(e) {
   e.preventDefault();

let name = document.querySelector('#name').value;
let phone = document.querySelector('#pnumber').value;
let partySize = document.querySelector('#partySize').value;

 //Show Alert Message
 document.querySelector('.alert').style.display = 'block';

 //Hide Alert Message After Seven Seconds
 setTimeout(function() {document.querySelector('.alert').style.display = 'none';
 }, 7000);
}