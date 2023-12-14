const CUSTOM_DATETIME_FORMAT = 'yyyy-MM-dd HH:mm:ss';
const shortenedUrlListTableElement = document.getElementById('shortenedUrlListTable');

var DateTime = luxon.DateTime;

// Main
setTimeout(() => {
    axios.get('/api/shortened-urls/')
        .then(function (response) {
            let dataScript = '';
            let responseData = response.data;
            responseData.forEach(element => {
                let id = element.id;
                let name = element.name;
                let sourceUrl = element.source_url;
                let targetUrl = element.target_url;
                let prefix = element.prefix;
                let createdTime = element.created_time;
                let updatedTime = element.updated_time;
                dataScript += `
                    <tr>
                        <td class="border-bottom-0">
                            <p class="mb-0 fw-normal">${id}</p>
                        </td>
                        <td class="border-bottom-0">
                            <a href="${window.location.origin}/shortened-urls/${id}" class="text-primary fw-normal">${name}</a>
                        </td>
                        <td class="border-bottom-0">
                            <p class="mb-0 fw-normal">${sourceUrl}</p>
                        </td>
                        <td class="border-bottom-0">
                            <a href="${window.location.origin}/${prefix}/${targetUrl}" class="text-primary fw-normal">${targetUrl}</a>
                        </td>
                        <td class="border-bottom-0">
                            <p class="mb-0 fw-normal">${prefix}</p>
                        </td>
                        <td class="border-bottom-0">
                            <p class="mb-0 fw-normal">${DateTime.fromISO(createdTime).toFormat(CUSTOM_DATETIME_FORMAT)}</p>
                        </td>
                        <td class="border-bottom-0">
                            <p class="mb-0 fw-normal">${DateTime.fromISO(updatedTime).toFormat(CUSTOM_DATETIME_FORMAT)}</p>
                        </td>
                    </tr>
                `;
            });

            shortenedUrlListTableElement.querySelector('tbody').innerHTML = dataScript;
        })
        .catch(function (error) {
            console.log(error);
        });
}, 2000);