document.addEventListener('DOMContentLoaded', function(){
    compose_post()
})

function compose_post(){
    const form = document.querySelector('form');
    const post = document.querySelector('#post');
    const submitBtn = document.querySelector('#submit');

    // setting for a new post
    post.value = '';
    submitBtn.disabled = true;
    post.onkeyup = function(){
        submitBtn.disabled = false;
    }

    // when user clicks submit, send POST request 
    form.onsubmit = function(){
        const content = post.value;
        fetch('/compose', {
            method: 'POST', 
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
        return false
    }
}

/* headers: {'X-CSRFToken': Cookies.get('csrftoken')}, */

