const dropdowns = document.querySelectorAll('.main_write__dropdown');
dropdowns.forEach((dropdown) => {
	const select = dropdown.querySelector('.main_write__select');
	const caret = dropdown.querySelector('.main_write__caret');
	const menu = dropdown.querySelector('.main_write__menu');
	const options = dropdown.querySelectorAll('.main_write__menu li');
	const selected = dropdown.querySelector('.main_write__selected');

	select.addEventListener('click', () => {
		select.classList.toggle('main_write__select-clicked');
		caret.classList.toggle('main_write__caret-rotate');
		menu.classList.toggle('main_write__menu-open');
	});
	options.forEach((option) => {
		option.addEventListener('click', () => {
			selected.innerText = option.innerText;
			select.classList.remove('main_write__select-clicked');
			caret.classList.remove('main_write__caret-rotate');
			menu.classList.remove('main_write__menu-open');
			options.forEach((option) => {
				option.classList.remove('main_write__active');
			});
			option.classList.add('main_write__active');
		});
	});
});
