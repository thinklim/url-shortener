/**
 * 브라우저의 쿠키 값을 가져옴
 * @param {string} name 
 * @returns {string}
 */
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const shortenedUrlNewFormElement = document.getElementById('shortenedUrlNewForm');
shortenedUrlNewFormElement.addEventListener('submit', event => {
    event.preventDefault();
    event.stopPropagation();

    shortenedUrlNewFormElement.classList.add('was-validated');

    if (shortenedUrlNewFormElement.checkValidity()) {
        let name = shortenedUrlNewFormElement.querySelector('#nameInput');
        let sourceUrl = shortenedUrlNewFormElement.querySelector('#sourceUrlInput');
        let description = shortenedUrlNewFormElement.querySelector('#descriptionInput');

        axios({
            method: 'post',
            url: '/api/shortened-urls/',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                name: name.value,
                source_url: sourceUrl.value,
                description: description.value,
            }
        }).then(response => {
            location.replace('/');
        }).catch(error => {
            console.log(error);
        })
    }
}, false)