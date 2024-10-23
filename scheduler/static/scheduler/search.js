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
            button.innerHTML = "Added to Calendar";
        }
    });
}

//https://codepen.io/jessewarddev/pen/LYVqabP