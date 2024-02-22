const profilePhotos = document.querySelectorAll('.profile-photo');
setTimeout(function() {
    profilePhotos.forEach(function(photo) {
        photo.classList.add('animate');
    });
}, 250);
function typeWriter(elementId) {
    const nameText = document.getElementById(elementId).textContent;
    document.getElementById(elementId).textContent = "";
    
    let index = 0;

    function type() {
        if (index < nameText.length) {
            document.getElementById(elementId).textContent += nameText.charAt(index);
            index++;
            setTimeout(type, 60);
        }
    }

    type();
}
typeWriter("name1");
typeWriter("name2");
typeWriter("name3");
typeWriter("name4");

const toggle = document.getElementById('toggleDark');
const body = document.querySelector('body');
const container = document.querySelector('.container');

toggle.addEventListener('click', function(){
    this.classList.toggle('bi-moon');
    if(this.classList.contains('bi-moon')){
        body.style.background = 'black';
        body.style.color = 'white';
        container.style.background = 'black';
        container.style.color = '#EEEEEE';
    } else {
        
        body.style.background = 'white';
        body.style.color = 'black';
        container.style.background = '#EEEEEE';
        container.style.color = 'black';
    }
});
