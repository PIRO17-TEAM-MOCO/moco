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

const modal = document.getElementById("post_write__modal");
const openModal = document.getElementById("main_write__register_modal_btn");
openModal.addEventListener("click", (e) => {
  modal.style.display = "block";
});

const closeModal = modal.querySelector(".post_write__modal__close_btn");
closeModal.addEventListener("click", (e) => {
  modal.style.display = "none";
});

modal.addEventListener("click", (e) => {
  const clickOverlay = e.target;
  if (clickOverlay.classList.contains("post_write__modal__overlay")) {
    modal.style.display = "none";
  }
});

/*function postWriteForm_check() {
  var contact = document.getElementById("main_write__select_contact");
  var duration = document.getElementById("main_write__select_duration");
  var number = document.getElementById("main_write__top__box_text_number");
  var location = document.getElementById("main_write__top__box_text_location");
  var applyLink = document.getElementById("main_write__top__box_text_link");
  var tag = document.getElementById("main_write__tag_write__main_content");
  var title = document.getElementById(
    "main_write__title_write__main_content_input"
  );
  var content = document.getElementById("main_write__content__write_txt");

  if (contact.value == "----------") {
    alert("진행방식을 선택해주세요.");
    contact.focus();
    return false;
  }

  if (duration.value == "----------") {
    alert("모임형태를 선택해주세요.");
    duration.focus();
    return false;
  }

  if (number.value <= 1 || number.value == "") {
    alert("모임 인원은 2명 이상으로 입력해주세요.");
    number.focus();
    return false;
  }

  if (location.value == "") {
    alert("지역을 입력해주세요.");
    location.focus();
    return false;
  }
*/

//var linkCheck = /(https:\/\/)(forms\.)(gle)(\/)([a-zA-Z0-9-])*/g;//
/*
  if (!linkCheck.test(applyLink.value)) {
    alert("구글폼 링크 형식에 맞춰 입력해주세요.");
    applyLink.focus();
    return false;
  }

  if (tag.value == "") {
    alert("태그를 입력해주세요.");
    tag.focus();
    return false;
  }

  if (title.value == "") {
    alert("제목을 입력해주세요.");
    title.focus();
    return false;
  }

  if (content.value == "") {
    alert("내용을 입력해주세요.");
    content.focus();
    return false;
  }
}
*/
