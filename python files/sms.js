const accountSid = 'AC222d9accf4275e0a382642ca769af586'; 
const authToken = '[3e478e164fad246b1b7144e4dbb0eb75]'; 
const client = require('twilio')(accountSid, authToken); 
 
client.messages 
      .create({         
         to: '+19199854106' 
       }) 
      .then(message => console.log(message.sid)) 
      .done();
