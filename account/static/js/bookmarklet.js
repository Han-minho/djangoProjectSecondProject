// 정적 파일 편집과 자바스크립트 코드 추가
const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
//최소 넓이와 최소 높이 설정
const minWidth = 250;
const minHeight = 250;

// CSS 로드
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);

// HTML 로드
var body = document.getElementsByTagName('body')[0];
boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');
    // 이미지 목록 초기화
    imagesFound.innerHTML = '';
    // 북마크릿 표시
    bookmarklet.style.display = 'block';
        // 닫기 이벤트
        bookmarklet.querySelector('#close')
            .addEventListener('click', function(){
            bookmarklet.style.display = 'none'
        });

        // 최소 크기를 갖는 DOM 내의 이미지 찾기
        images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
        images.forEach(image => {
            if(image.naturalWidth >= minWidth&& image.naturalHeight >= minHeight)
            {
                var imageFound = document.createElement('img');
                imageFound.src = image.src;
                imagesFound.append(imageFound);
            }
        })
    }
// 북마크릿 실행
bookmarkletLaunch();