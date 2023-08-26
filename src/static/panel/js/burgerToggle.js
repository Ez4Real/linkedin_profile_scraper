const burgerIcon = document.querySelector('.burger-icon');
const menu = document.querySelector('.menu');

burgerIcon.addEventListener('click', () => {
    menu.classList.toggle('active');
    burgerIcon.classList.toggle('active');
});

function toggleStyles(element) {
    if (element.classList.contains("clicked")) {
        element.classList.remove("clicked");
    } else {
        element.classList.add("clicked");
    }
}