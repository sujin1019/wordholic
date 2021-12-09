const backToTop = document.getElementById('backtotop');

const checkScroll = () => {
    // 웹페이지가 수직으로 얼마나 스크롤되었는지를 확인 - 픽셀단위로 반환
    let pYOffset = window.pageYOffset;

    if (pYOffset !== 0) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
}

const moveBackToTop = () => {
    if (window.pageYOffset > 0) {
        // smooth하게 scroll하기
        window.scrollTo({top: 0, behavior: "smooth"});
    }
}

window.addEventListener('scroll', checkScroll);
backToTop.addEventListener('click', moveBackToTop);

/* ----------------------------------------------------- */

const slidePrevList = document.getElementsByClassName('slide-prev');

function transformNext (event) {
    const slideNext = event.target;
    const slidePrev = slideNext.previousElementSibling;

    const classList = slideNext.parentElement.parentElement.nextElementSibling;
    let activeLi = classList.getAttribute('data-position');
    const liList = classList.getElementsByTagName('li');

    // 하나의 카드라도 왼쪽으로 이동했다면, 오른쪽으로 갈 수 있음
    if (Number(activeLi) < 0) {
        activeLi = Number(activeLi) + 260;

        // 왼쪽에 있던 카드가 오른쪽으로 갔다면, 다시 왼쪽으로 갈 수 있으므로 prev 버튼 활성화
        slidePrev.style.color = '#2f3059';
        slidePrev.classList.add('slide-prev-hover');
        slidePrev.addEventListener('click', transformPrev);

        // 맨 왼쪽에 현재 보이는 카드가, 맨 첫번째 카드라면, next로 갈 수 없으므로 next 버튼 비활성화
        if (Number(activeLi) === 0) {
            slideNext.style.color = '#cfd8dc';
            slideNext.classList.remove('slide-next-hover');
            slideNext.removeEventListener('click', transformNext);
        }
    }
    
    classList.style.transition = 'transform 1s';
    classList.style.transform = 'translateX(' + String(activeLi) + 'px)';
    classList.setAttribute('data-position', activeLi);
}

function transformPrev(event) {
    const slidePrev = event.target;
    const slideNext = slidePrev.nextElementSibling;

    // ul 태그 선택
    const classList = slidePrev.parentElement.parentElement.nextElementSibling;
    let activeLi = classList.getAttribute('data-position');
    const liList = classList.getElementsByTagName('li');

    if (classList.clientWidth < (liList.length * 260 + Number(activeLi))) {
        // 위치를 왼쪽으로 260 이동
        activeLi = Number(activeLi) - 260;

        // activeLi 값보다 classList.clientWidth (ul 태그의 너비)가 크다는 것은
        // 넘치는 li가 없다는 뜻으로, Next 버튼 비활성화
        if (classList.clientWidth > (liList.length * 260 + Number(activeLi))) {
            slidePrev.style.color = '#cfd8dc';
            slidePrev.classList.remove('slide-prev-hover');
            slidePrev.removeEventListener('click', transformPrev);
        }

        slideNext.style.color = '#2f3059';
        slideNext.classList.add('slide-next-hover');
        slideNext.addEventListener('click', transformNext);
    }

    classList.style.transition = 'transform 1s';
    classList.style.transform = 'translateX(' + String(activeLi) + 'px)';
    classList.setAttribute('data-position', activeLi);
}

for (let i = 0; i < slidePrevList.length; i++) {
    // ul 태그 선택
    let classList = slidePrevList[i].parentElement.parentElement.nextElementSibling;
    let liList = classList.getElementsByTagName('li');

    // 카드가 ul 태그 너비보다 넘치면 prev 버튼은 활성화하고, next 는 현재 맨 첫카드 위치이므로 비활성화

    if (classList.clientWidth < (liList.length * 260)) {
        slidePrevList[i].classList.add('slide-prev-hover');
        slidePrevList[i].addEventListener('click', transformPrev);
    } else {
        const arrowContainer = slidePrevList[i].parentElement;
        arrowContainer.removeChild(slidePrevList[i].nextElementSibling);
        arrowContainer.removeChild(slidePrevList[i]);
    }

}

/* ----------------------------------------------------- */

let touchstartX; // drag한 시점의 마우스 위치 - 최초 요소의 X 좌표값
let currentClassList; // drag한 시점과 관련된 class list
let currentImg; // drag한 시점에서의 해당 이미지
let currentActiveLi; // 마우스를 drag하기 시작할 때의 카드의 위치 (원래의 위치)
let nowActiveLi; // drag하면서 변경되는 카드의 위치
let mouseStart; // drag가 시작된 상황인지 나타내는 boolean

function processTouchMove (event) {
    event.preventDefault();

    let currentX = event.clientX || event.touches[0].screenX; // 지금의 위치
    // 이동해야 할 값
    nowActiveLi = Number(currentActiveLi) + (Number(currentX) - Number(touchstartX));
    // 바로 즉시 마우스 위치에 따라 카드를 이동함
    currentClassList.style.transition = 'transform 0s linear';
    currentClassList.style.transform = 'translateX(' + String(nowActiveLi) + 'px)';
}

function processTouchStart(event) {
    mouseStart = true;
    // 해당 요소의 고유 동작을 중단시키는 함수 (이미지만 드래드로 이동하는 고유 동작 중단)
    event.preventDefault();
    touchstartX = event.clientX || event.touches[0].screenX;
    currentImg = event.target;

    // 드래그 처리를 위해 드래그 중(mousemove), 드래그가 끝났을 때(mouseup)에 이벤트를 걸어줌
    // PC
    currentImg.addEventListener('mousemove', processTouchMove);
    currentImg.addEventListener('mouseup', processTouchEnd);
    // Mobile
    currentImg.addEventListener('touchmove', processTouchMove);
    currentImg.addEventListener('touchend', processTouchEnd);


    currentClassList = currentImg.parentElement.parentElement;
    currentActiveLi = currentClassList.getAttribute('data-position');
}

function processTouchEnd(event) {
    event.preventDefault();

    if (mouseStart === true) {
        // PC
        currentImg.removeEventListener('mousemove', processTouchMove);
        currentImg.removeEventListener('mouseup', processTouchEnd);
        // Mobile
        currentImg.removeEventListener('touchmove', processTouchMove);
        currentImg.removeEventListener('touchend', processTouchEnd);

        // 맨 처음 카드가 맨 앞에 배치되도록 초기 상태로 이동
        currentClassList.style.transition = 'transform 1s ease';
        currentClassList.style.transform = 'translateX(0px)';
        currentClassList.setAttribute('data-position', 0);
    
        // 맨 처음 카드가 맨 앞에 배치된 상태로 화살표 버튼도 초기 상태로 변경
        let eachSlidePrev = currentClassList.previousElementSibling.children[1].children[0];
        let eachSlideNext = currentClassList.previousElementSibling.children[1].children[1];
        let eachLiList = currentClassList.getElementsByTagName('li');
    
        if (currentClassList.clientWidth < (eachLiList.length * 260)) {
            eachSlidePrev.style.color = '#2f3059';
            eachSlidePrev.classList.add('slide-prev-hover');
            eachSlidePrev.addEventListener('click', transformPrev);
    
            eachSlideNext.style.color = '#cfd8dc';
            eachSlideNext.classList.remove('slide-next-hover');
            eachSlideNext.removeEventListener('click', transformNext);
        } else {
            // 카드가 ul 태그 너비보다 넘치지 않으면 prev, next 버튼이 불필요하므로 아예 삭제함
            // 태그 삭제 시 부모 요소에서 removeChild를 통해 삭제해야 함
            const eachViewAllNode = slidePrev.parentNode;
            eachViewAllNode.removeChild(slidePrev.nextElementSibling);
            eachViewAllNode.removeChild(slidePrev);
        }
    }

    mouseStart = false;
}

// 특정 요소를 드래그하다가, 요소 밖에서 드래그를 끝낼 수 있으므로, window에 이벤트를 걸어줌
window.addEventListener('dragend', processTouchEnd);
window.addEventListener('mouseup', processTouchEnd);

// interface간의 오작동을 막기 위햐 카드 내의 이미지에만 드래그 인터페이스를 제공하기로 함
const classImgLists = document.querySelectorAll('ul li img');

for (let i = 0; i < classImgLists.length; i++) {
    // 해당 요소에 마우스를 누르면, 드래그를 시작할 수 있으므로, 이벤트를 걸어줌
    classImgLists[i].addEventListener('mousedown', processTouchStart); // PC
    classImgLists[i].addEventListener('touchstart', processTouchStart); // Mobile
}

/* ----------------------------------------------- */

// Vue JS
const app = new Vue({
    el: "#app",
    data: {
        selected: '',
        answer: ''
    },
    methods: {
        reloadPage: () => {
            window.location.reload();
        },
        showHint: (event) => {
            let target = event.target.getAttribute('data-id')
            axios("http://localhost:8081/quiz/kanji/hint", {
                method: "get",
                params: {
                    row_id: target
                } 
            })
            .then((response) => {
                event.target.previousElementSibling.value = response.data.hint
            })
            .catch((error) => {
                console.log(error);
            })
        }
    }
});
