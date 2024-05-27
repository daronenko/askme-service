const answers = document.querySelectorAll('answer.card')

for (const answer of answers) {
    const correctCheckbox = answer.querySelector('.answer-checkbox')
    const answerId = correctCheckbox.dataset.answerId
    
    correctCheckbox.addEventListener('change', () => {
        const request = new Request('/answer/correct', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                answer_id: answerId,
                is_correct: correctCheckbox.checked,
            })
        })

        fetch(request)
            .then((response) => response.json())
    })
}
