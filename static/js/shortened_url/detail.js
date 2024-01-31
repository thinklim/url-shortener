import {getCookie} from '../util.js';

const csrftoken = getCookie('csrftoken');
const shortenedUrlDetailFormElement = document.getElementById('shortenedUrlDetailForm');
const shortenedUrlNameInputElement = shortenedUrlDetailFormElement.querySelector('#nameInput');
const shortenedUrlSourceUrlInputElement = shortenedUrlDetailFormElement.querySelector('#sourceUrlInput');
const shortenedUrlDescriptionInputElement = shortenedUrlDetailFormElement.querySelector('#descriptionInput');
const shortenedUrlPrefixInputElement = shortenedUrlDetailFormElement.querySelector('#prefixInput');
const shortenedUrlTargetUrlInputElement = shortenedUrlDetailFormElement.querySelector('#targetUrlInput');
const shortenedUrlCreatedTimeInputElement = shortenedUrlDetailFormElement.querySelector('#createdTimeInput');
const shortenedUrlUpdatedTimeInputElement = shortenedUrlDetailFormElement.querySelector('#updatedTimeInput');
const placeholderElements = document.querySelectorAll('.placeholder-glow');
const urlPathname = location.pathname;

setTimeout(() => {
    axios.get(`/api${urlPathname}`)
        .then(response => {
            shortenedUrlDetailFormElement.querySelectorAll('.d-none').forEach(element => {
                element.classList.remove('d-none');
            })

            placeholderElements.forEach(placeholderElement => {
                placeholderElement.classList.add('d-none');
            });

            let responseData = response.data;
            shortenedUrlNameInputElement.value = responseData['name'];
            shortenedUrlSourceUrlInputElement.value = responseData['source_url'];
            shortenedUrlDescriptionInputElement.value = responseData['description'];
            shortenedUrlPrefixInputElement.value = responseData['prefix'];
            shortenedUrlTargetUrlInputElement.value = responseData['target_url'];
            shortenedUrlCreatedTimeInputElement.value = responseData['created_time'];
            shortenedUrlUpdatedTimeInputElement.value = responseData['updated_time'];
        })
        .catch(error => {
            console.log(error);
        });    
}, 1000);

// Event

shortenedUrlDetailFormElement.addEventListener('submit', (event) => {
    event.preventDefault();
    event.stopPropagation();

    shortenedUrlDetailFormElement.classList.add('was-validated');

    if (shortenedUrlDetailFormElement.checkValidity()) {
        let name = shortenedUrlNameInputElement.value;
        let sourceUrl = shortenedUrlSourceUrlInputElement.value;
        let description = shortenedUrlDescriptionInputElement.value;

        axios({
            method: 'patch',
            url: `/api${urlPathname}`,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                name: name,
                source_url: sourceUrl,
                description: description
            }
        }).then(response => {
            alert('수정했습니다.');
        }).catch(error => {
            console.log(error);
        })
    }
});
