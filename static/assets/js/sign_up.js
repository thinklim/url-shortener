(() => {
    'use strict'

    const signUpForm = document.getElementById('signUpForm');
    const emailInputElement = document.getElementById('emailInput');
    const password1InputElement = document.getElementById('password1Input');
    const password2InputElement = document.getElementById('password2Input');
    const emailErrorMessageElement = document.getElementById('emailErrorMessageDiv');
    const password1ErrorMessageElement = document.getElementById('password1ErrorMessageDiv');
    const password2ErrorMessageElement = document.getElementById('password2ErrorMessageDiv');

    signUpForm.addEventListener('submit', event => {
        let isPasswordMatch = (password2InputElement.value !== '') && (password1InputElement.value === password2InputElement.value);

        if (!signUpForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        if (emailInputElement.validity.valueMissing) {
            emailErrorMessageElement.textContent = '이메일을 입력하세요.'
        }

        if (emailInputElement.validity.typeMismatch) {
            emailErrorMessageElement.textContent = '이메일 형식으로 입력하세요.'
        }

        if (password1InputElement.validity.valueMissing || password1InputElement.validity.tooShort) {
            password1ErrorMessageElement.textContent = '비밀번호는 8글자 이상입니다.'
        }

        if (!isPasswordMatch) {
            password2InputElement.setCustomValidity('비밀번호가 다릅니다.');
            password2ErrorMessageElement.textContent = '비밀번호가 다릅니다';
        } else {
            password2InputElement.setCustomValidity('');
        }

        signUpForm.classList.add('was-validated')
    }, false);
})()