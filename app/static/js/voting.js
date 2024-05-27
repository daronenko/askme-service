const components = document.querySelectorAll('question.card, answer.card')

for (const component of components) {
    const scoreValue = component.querySelector('.score')
    const voteButtons = component.querySelectorAll('button')

    for (const voteButton of voteButtons) {
        voteButton.addEventListener('click', () => {
            const request = new Request('/vote/', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    action: voteButton.dataset.action,
                    component: scoreValue.dataset.component,
                    component_id: Number(scoreValue.dataset.componentId),
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => scoreValue.innerHTML = data.rating)
        })
    }
}
