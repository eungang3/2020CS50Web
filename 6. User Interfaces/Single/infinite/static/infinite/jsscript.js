let counter = 1;

const quantity = 20;

document.addEventListener('DOMContentLoaded', load);

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight){
        load();
    }
};

function load(){
    const start = counter;
    const end = start + quantity - 1;

    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
    })
};

function add_post(contents){
    const post = document.createElement('div')
    post.className = 'post';
    post.innerHTML = contents;
    document.querySelector('#posts').append(post);
}