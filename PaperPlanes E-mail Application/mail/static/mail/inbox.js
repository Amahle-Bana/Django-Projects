document.addEventListener("DOMContentLoaded", function() {

    // Use buttons to toggle between views
    document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
    document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
    document.querySelector("#archived").addEventListener("click", () => load_mailbox("archived"));
    document.querySelector("#compose").addEventListener("click", compose_email);

    // Submit handler
    document.querySelector("#compose-form").addEventListener("submit", send_email);

    // By default, load the inbox
    load_mailbox("inbox");
});

function compose_email() {

    //Show compose view and hide other views
    document.querySelector("#emails-view").style.display = "none";
    document.querySelector("#compose-view").style.display = "block";
    document.querySelector("#email-detail-view").style.display = "none";

    // Clear out composition fields
    document.querySelector("#compose-recipients").value = '';
    document.querySelector("#compose-subject").value = '';
    document.querySelector("#compose-body").value = '';
}
function view_email(id) {
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print Email
        console.log(email);

        document.querySelector("#emails-view").style.display = "none";
        document.querySelector("#compose-view").style.display = "none";
        document.querySelector("#email-detail-view").style.display = "block";

        document.querySelector("#email-detail-view").innerHTML = `
            <div class="emailFromDetail">
                <p class="emailFromDetailParagraph">From: </p>
                <strong class="emailFromDetailInput">${email.sender}</strong>
            </div>
            <div class="emailSubjectDetail">
                <p class="emailSubjectDetailParagraph">Subject: </p>
                <strong class="emailSubjectDetailInput">${email.subject}</strong>
            </div>
            <div class="emailTextDetail">
                <strong disabled class="emailTextDetailTextarea" id="compose-body">${email.body}</textarea>
            </div>
            <div class="emailTimeDetail">
                <p disabled class="emailTimeDetailParagraph">${email.timestamp1}</p>
            </div>
            `

            // Change to read 
            if (!email.read) {
                fetch(`/emails/${email.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        read: true
                    })
                })
            }

            // Archive/Unarchive Topic
            const archiveButton = document.createElement('button');
            archiveButton.innerHTML = email.archived ? 'Unarchive': 'Archive';
            archiveButton.className = 'emailActionDetailArchive';
            archiveButton.addEventListener("click", function() {
                fetch(`/emails/${email.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: !email.archived
                    })
                })
                .then(() => { load_mailbox('archive')})
            });
            document.querySelector("#email-detail-view").append(archiveButton);

            // Reply Logic
            const replyButton = document.createElement('button');
            replyButton.innerHTML = "Reply";
            replyButton.className = "emailActionDetailReply";
            replyButton.addEventListener("click", function() {
                compose_email();
                document.querySelector("#compose-recipients").value = email.sender;
                let subject = email.subject;
                if (subject.split(' ', 1)[0] != "Re:") {
                    subject = "Re: " + email.subject;
                }
                document.querySelector("#compose-subject").value = subject;
                document.querySelector("#compose-body").value = email.body;
            });
            document.querySelector("#email-detail-view").append(replyButton);
        });
    }

function load_mailbox(mailbox) {

    // Show the railbox and hide other views
    document.querySelector("#emails-view").style.display = "block";
    document.querySelector("#compose-view").style.display = "none";
    document.querySelector("#email-detail-view").style.display = "none";

    // Show the mailbox more
    document.querySelector('#emails-view').innerHTML = `<h3 class="mailboxHeader">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        //Print emails
        emails.forEach(singleEmail => {

            console.log(singleEmail);

            // Create div for each email
            const newEmail = document.createElement("div");
            newEmail.className = `emailItem1`;
            newEmail.innerHTML = `
            <h4 class="emailFrom">${singleEmail.sender_username}</h4>
            <div class="emailSubject"><h4>${singleEmail.subject} -</h4><p>${singleEmail.body}</p></div>
            <h4 class="emailTime">${singleEmail.timestamp2}</h4>
            `;
            
            // Change background-color
            newEmail.className = singleEmail.read ? 'emailItem2': 'emailItem1';

            // Add check event to view email
            newEmail.addEventListener("click", function() {
                view_email(singleEmail.id)
            });
            document.querySelector("#emails-view").append(newEmail);
        })
        // ... do something else with emails
    });
}

function send_email(event) {
    event.preventDefault();
    
    // Store fields
    const recipient = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch("/emails", {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipient,
            subject: subject,
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        //Print result
        console.log(result);
    });
}