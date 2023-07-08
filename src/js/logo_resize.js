window.addEventListener('load', function() {
    var logoImg = document.getElementById('logo-img');
    var windowWidth = window.innerWidth;
    var logoSize = windowWidth * 0.13;

    logoImg.style.width = logoSize + 'px';
    logoImg.style.height = 'auto';
});

window.addEventListener('resize', function() {
    var logoImg = document.getElementById('logo-img');
    var windowWidth = window.innerWidth;
    var logoSize = windowWidth * 0.13;

    logoImg.style.width = logoSize + 'px';
    logoImg.style.height = 'auto';
});
