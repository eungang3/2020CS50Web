document.addEventListener('DOMContentLoaded', function(){
    compose_post();
    load_posts('all');
    document.querySelector('#all').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));
})

function load_posts(posttype){
    // change the title according to the post type
    let title;
    if (posttype === 'all'){
        title = 'All Posts';
    }
    else {
        title = 'Following';
    }
  document.querySelector('#title').innerHTML = `<h3>${title}</h3>`;

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
        document.querySelector('#post-view').insertAdjacentHTML("afterbegin", postBlock);
        }
    })
}

function compose_post(){
    const form = document.querySelector('#compose-form');
    const post = document.querySelector('#post-content');
    const submitBtn = document.querySelector('#submit');

    // if logged in, setting for a new post
    if(form && post && submitBtn){
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

