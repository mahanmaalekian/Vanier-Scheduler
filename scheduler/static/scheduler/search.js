function addToCalendar(exam)
{
    console.log("inside add to calendar");
    const button = document.getElementById(exam);
    const courseId = exam.split(" ")[0];
    const sections = exam.split(" ")[1];
    console.log(courseId);
    console.log(sections);

    fetch('/add_to_calendar', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Include the CSRF token here
        },
        body: JSON.stringify({
            courseId: courseId,
            sections: sections
        })
    })
    .then(response => {
        if(response.status != 200){
            return response.json().then(errorData => {
                alert(errorData.error);
            })
        }
        else{
            button.innerHTML = "Added";
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//https://codepen.io/jessewarddev/pen/LYVqabP