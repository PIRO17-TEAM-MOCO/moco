const mobile = document.querySelector('.navbar-mobile');
const toggleBtn = mobile.querySelector('.navbar__toggle');
const menu = mobile.querySelector('.navbar__menu');

toggleBtn.addEventListener('click', () => {
  menu.classList.toggle('active');
});

const toggleBtnMenu = menu.querySelector('.navbar__menu__toggle');
const icon = toggleBtnMenu.querySelector('.fa-solid');
const dropmenu = menu.querySelector('.base__dropmenu');

toggleBtnMenu.addEventListener('click', () => {
  dropmenu.classList.toggle('active');
  if (icon.className == 'fa-solid fa-angle-down')
    icon.className = 'fa-solid fa-angle-up';
  else
    icon.className = 'fa-solid fa-angle-down';
});