// Новый код
document.addEventListener('DOMContentLoaded', () => {
    localStorage.clear();

    const category = document.querySelector('#id_category');
    const service = document.querySelector('#id_usluga');
    const quantity = document.querySelector('#customRange2');
    const rangeValue = document.querySelector('#rangeValue');
    const masters = document.querySelector('#id_master');
    const date = document.querySelector('#zayavka_date');
    const address = document.querySelector('#address');
    const comment = document.querySelector('#order_comment');
    const submitButton = document.querySelector('#submitOrderButton');

    setDefaultValues(category.value, service.value, quantity.value, masters.value);

    category.addEventListener('change', () => {
        fetch(`/api/get_services_by_category/?category_id=${category.value}`)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const parsedDocument = parser.parseFromString(html, 'text/html');
                service.innerHTML = parsedDocument.querySelector('select#id_usluga').innerHTML;
                masters.innerHTML = parsedDocument.querySelector('select#id_master').innerHTML;
                const category_id = localStorage.getItem(`category_${category.value}`);
                if (category_id === null) {
                    add_services_by_other_category(category.value, service.children[0].value, masters.value);
                } else {
                    load_and_update_services(category_id, service.value, masters.value);
                }
            })
    });

    service.addEventListener('change', () => {
        load_and_update_services(category.value, service.value, masters.value);
    });

    quantity.addEventListener('change', () => {
        let services = JSON.parse(localStorage.getItem(`category_${category.value}`));
        services[`service_${service.value}`] = quantity.value;
        localStorage.setItem(`category_${category.value}`, JSON.stringify(services));
        rangeValue.innerHTML = quantity.value;
    });

    date.addEventListener('input', () => {
        localStorage.setItem('date_document', date.value);
    });

    address.addEventListener('input', () => {
        localStorage.setItem('address', address.value);
    });

    masters.addEventListener('change', () => {
        localStorage.setItem('master', masters.value);
    });

    submitButton.addEventListener('click', function (event) {
        event.preventDefault();
        const data = {
            categories: {},
            address: localStorage.getItem('address'),
            comment: comment.value,
            master: localStorage.getItem('master'),
            date_document: localStorage.getItem('date_document')
        };
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key) && key.startsWith('category_')) {
                let categories = JSON.parse(localStorage.getItem(key));
                for (let item in categories) {
                    if (categories[item] === '0') {
                        delete categories[item];
                    }
                }
                data['categories'][key] = categories;
            }
        }
        const csrfToken = getCSRFToken(document);
        xhrRequest('POST', '/zayavki/', csrfToken, success, data);

        function success() {
            localStorage.clear();
            window.location = window.location;
        }
    });

    function setDefaultValues(category_id, service_id, quantity_value, master_id) {
        const data = {
            [`service_${service_id}`]: `${quantity_value}`,
        }
        localStorage.setItem(`category_${category_id}`, JSON.stringify(data));
        localStorage.setItem('master', master_id);
    }

    function load_and_update_services(category_id, service_id, master_id) {
        let service_quantity = JSON.parse(localStorage.getItem(`category_${category_id}`));
        if (service_quantity !== null) {
            if (service_quantity[`service_${service_id}`] === undefined) {
                quantity.value = 0;
                rangeValue.innerHTML = '0';
            } else {
                quantity.value = service_quantity[`service_${service.value}`];
                rangeValue.innerHTML = service_quantity[`service_${service.value}`];
            }
            service_quantity[`service_${service_id}`] = quantity.value;
            localStorage.setItem(`category_${category_id}`, JSON.stringify(service_quantity));
        } else {
            service_quantity = JSON.parse(localStorage.getItem(`category_${category.value}`));
            quantity.value = service_quantity[`service_${service.children[0].value}`];
            rangeValue.innerHTML = service_quantity[`service_${service.children[0].value}`];
        }
        localStorage.setItem('master', master_id);
    }

    function add_services_by_other_category(category_id, service_id, master_id) {
        quantity.value = 0;
        rangeValue.innerHTML = '0';
        const data = {
            [`service_${service_id}`]: `${quantity.value}`
        }
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key) && key.startsWith('category_')) {
                localStorage.removeItem(key);
            }
        }
        localStorage.setItem(`category_${category_id}`, JSON.stringify(data));
        localStorage.setItem('master', master_id);
    }

    function xhrRequest(method='POST', url, csrfToken, successFunction, data) {
        const xhr = new XMLHttpRequest();

        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onload = function() {
            if (xhr.status === 200) {
                successFunction();
            } else {
                console.error('Произошла ошибка. Статус:', xhr.status);
            }
        };

        xhr.send(JSON.stringify(data));
    }

    function getCSRFToken(doc) {
        let csrf = doc.cookie.toString();
        csrf = csrf.slice(csrf.indexOf('csrftoken='), csrf.length).split(';')[0].substring(10);
        return csrf
    }
});