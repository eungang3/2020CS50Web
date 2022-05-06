document.addEventListener('DOMContentLoaded', function(){
    all_view = document.querySelector('#all-view');
    profile_view = document.querySelector('#profile-view');
    following_view = document.querySelector('#following-view');

    if (all_view){
        load_posts('all');
    }

    if (profile_view){
        load_posts('profile');
    }

    if (following_view){
        load_posts('following');
    }
    
    document.querySelector('#all').addEventListener('click', () => load_posts('all'));
    document.querySelector('#profile').addEventListener('click', () => load_posts('profile'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));
})

function load_posts(posttype){
    if (posttype == 'all'){
        all_view.innerHTML = '';
        compose_post();
    }
    // send get request for mails
    fetch(`/load_posts/${posttype}`)
    .then(response => response.json())
    .then(posts => {
        for (post of posts){
            const postBlock = `<div id="post" class="border rounded p-3 mb-2">
            <h5 id="writer" class="card-title">${post.writer}</h5>
            <a class="mb-2 text-primary" href="/">Edit</a>
            <p id="content" class="card-text">${post.content}</p>
            <p id="timestamp" class="card-text text-muted">${post.timestamp}</p>
            <a href="/">
                <i class="fa fa-heart unselected"></i> 0
            </a>
            </div>`
            document.querySelector(`#${posttype}-view`).insertAdjacentHTML("afterbegin", postBlock);
            }
        })
    return false;
}

function compose_post(){
    const form = document.querySelector('#compose-form');
    const post = document.querySelector('#post-content');
    const submitBtn = document.querySelector('#submit');

    // if logged in, setting for a new post
    if(form){
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
                console.log(result);
                load_posts('all');
            })
            
            // clear fields
            post.value = '';
            submitBtn.disabled = true;
            return false
        }
    }
    // if user is not logged in
    return false
}

/* headers: {'X-CSRFToken': Cookies.get('csrftoken')}, */

