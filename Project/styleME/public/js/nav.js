//buttons
const navOpen = document.querySelector('#navOpen');
const navClose = document.querySelector('#navClose');
//elements
const innerNav = document.querySelector('.inner-nav');
const mobileNavDarken = document.querySelector('.mobile-nav-darken');

navOpen.addEventListener('click', function () {
    innerNav.classList.remove('fadeOut')
    innerNav.classList.add('visible');
    mobileNavDarken.classList.add('visible');
});

navClose.addEventListener('click', function () {
    innerNav.classList.add('fadeOut');
    mobileNavDarken.classList.remove('visible');
});