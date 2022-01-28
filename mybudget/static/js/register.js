const usernameField = document.querySelector('#usernameField');
const messageArea = document.querySelector(".invalid-message");
const emailField = document.querySelector('#emailField');
const emailMessageArea = document.querySelector(".emailMessageArea");
const submitBtn = document.querySelector(".submit-btn")

usernameField.addEventListener('keyup', (event)=> {
    const usernameValue = event.target.value;

    usernameField.classList.remove("is-invalid");
    messageArea.style.display = "none";

    usernameField.classList.remove("is-invalid");
    emailMessageArea.style.display = "none";

    if(usernameValue.length > 0){
        fetch('/authentication/validate-username', {
            body:JSON.stringify({username: usernameValue}),
            method: "POST",
        }).then(res=>res.json()
        .then(data=>{
            if(data.username_error){
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                messageArea.style.display = "block";
                messageArea.style.color= "#FF325D";
                messageArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        }));
    }
})


emailField.addEventListener('keyup', (event) => {
    const emailValue = event.target.value;

    emailField.classList.remove("is-invalid");
    emailMessageArea.style.display = "none";

    if(emailValue.length > 0){
        fetch('/authentication/validate-email', {
            body:JSON.stringify({email: emailValue}),
            method: "POST",
        }).then(res=>res.json()
        .then(data=>{
            console.log('data', data)
            if(data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailMessageArea.style.display = "block";
                emailMessageArea.style.color= "#FF325D";
                emailMessageArea.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        }));
    }

})

