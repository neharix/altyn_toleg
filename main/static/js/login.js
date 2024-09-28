let number = document.querySelector("#number");
let accept_btn = document.querySelector("#accept-btn");

function validate_number() {
    let status = true;
    try {
        if (number.value.length != 8) {
            status = false;
        }
        if (status) {
            if (accept_btn.classList.contains("disabled")) {
                accept_btn.classList.remove("disabled");
            }
        }
        else {
            if (accept_btn.classList.contains("disabled") == false) {
                accept_btn.classList.add("disabled");
            }
        }
    }
    catch {
        if (accept_btn.classList.contains("disabled") == false) {
            accept_btn.classList.add("disabled");
        }
    }
}
number.onkeyup = validate_number;
number.onkeydown = validate_number;