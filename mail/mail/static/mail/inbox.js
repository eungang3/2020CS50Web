document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#each-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  const form = document.querySelector('form');
  
  // if it's reply 
  if (arguments.length === 4){
    // subject, body, timestamp, sender
    document.querySelector('#compose-recipients').value = `${arguments[3]}`;
    document.querySelector('#compose-subject').value = `RE: ${arguments[1]}`;
    document.querySelector('#compose-body').value = `On ${arguments[3]} ${arguments[4]} wrote: ${arguments[2]}`;
  } 

  // when user submits the form
  form.onsubmit = function(){
    
    // get the form values
    const recipients = document.getElementById('compose-recipients').value;
    const subject = document.getElementById('compose-subject').value;
    const body = document.getElementById('compose-body').value;

    // send post request with the values
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
      load_mailbox('sent');
      })
    return false;
  }
}



function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#each-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // send get request for mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // prepare a table
    const table = document.createElement('table');
    table.className = 'table';
    const thead = document.createElement('thead');
    table.append(thead);
    const tr = document.createElement('tr');
    thead.append(tr);
    // render title
    const titles = ['sender', 'subject', 'recipients', 'time']
    for (const title of titles){
      if (mailbox == 'sent' && title == 'sender'){
        continue;
      }
      const th = document.createElement('th');
      th.scope='col';
      th.innerHTML = title
      tr.append(th);
    }

    const tbody = document.createElement('tbody');
    table.append(tbody);

    for (let email of emails){
      // get values
      const subject = email['subject'];
      const sender = email['sender'];
      const recipients = email['recipients'];
      const timestamp = email['timestamp'];
      const read = email['read'];
      const id = email['id'];
      
      // prepare tr
      const tr = document.createElement('tr');
      tr.id = id;
      tbody.append(tr);

      // fill td with values
      const elements = {'subject': subject, 'sender':sender, 'recipients':recipients, 'timestamp':timestamp}
      for (element in elements){
        if (mailbox == 'sent' && element == 'sender'){
          continue;
        }
        const td = document.createElement('td');
        td.innerHTML = elements[element];
        if (read){
          td.className = 'table-secondary';
        }

        tr.append(td);
      }

      // if a row is clicked, call load_email function
      tr.onclick = function(){
        return load_email(id)
      }
    }
    // add newly created td to tr
    document.querySelector('#emails-view').append(table);
    })
  return false;
}

function load_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    const each_email_view = document.querySelector('#each-email-view');
    each_email_view.style.display = 'block';
    each_email_view.innerHTML = '';
    document.querySelector('#emails-view').style.display = 'none';

    // create html
    const items = {'sender': email['sender'], 'recipients':email['recipients'], 'subject':email['subject'], 'timestamp':email['timestamp']};
    
    // create header of mail
    for (let [key, value] of Object.entries(items)){
      const head = document.createElement('div');
      head.innerHTML = `<strong>${key}:</strong> ${value}`;
      each_email_view.append(head);
    }
    // make reply button
    const btn = document.createElement('button');
    btn.innerHTML = 'Reply';
    btn.className = 'btn btn-outline-primary';
    each_email_view.append(btn);
    
    // add event listener to reply button
    btn.onclick = function(){
      return compose_email(email['subject'], email['body'], email['timestamp'], email['sender']);
    }

    // make archive button
    const abtn = document.createElement('button');
    if (email['archived']){
      abtn.innerHTML = 'Unarchive';
      abtn.className = 'btn btn-outline-secondary';
      abtn.onclick = function(){
        unarchive(id);
        window.location.reload()
        load_mailbox('inbox');
      }
    }
    else{
      abtn.innerHTML = 'Archive';
      abtn.className = 'btn btn-outline-primary';
      abtn.onclick = function(){
        archive(id);
        alert('Archived successfully');
        window.location.reload()
        load_mailbox('inbox');
      }
    }
    each_email_view.append(abtn);

    // create body of mail
    const hr = document.createElement('hr');
    each_email_view.append(hr);
    const body = document.createElement('div');
    body.innerHTML = email['body'];
    each_email_view.append(body);

    // change email as read
    mark_as_read(id)
  });
}

function mark_as_read(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function archive(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
}

function unarchive(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
}
