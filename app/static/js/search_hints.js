const searchInput = document.getElementById('search-input');
const hintsContainer = document.getElementById('hints-container');

const debounceDelay = 400;

searchInput.addEventListener('input', function(event) {
    hintsContainer.innerHTML = '';
    hintsContainer.style.display = 'none';
});

searchInput.addEventListener('input', _.debounce(function() {
    const query = searchInput.value.trim();

    if (query === '') {
        hintsContainer.innerHTML = '';
        hintsContainer.style.display = 'none';
        return;
    }

    fetch(`/search/hints/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            hintsContainer.innerHTML = '';
            data.forEach(hint => {
                const hintElement = document.createElement('li');
                const link = document.createElement('a');
                link.classList.add('dropdown-item');
                link.href = `/search/?q=${hint}`;
                link.innerText = hint;
                hintElement.appendChild(link);
                hintsContainer.appendChild(hintElement);
            });

            if (data.length) {
                hintsContainer.style.display = 'block';
                console.log(data);
            } else {
                hintsContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching search hints:', error);
        });
}, debounceDelay));

document.addEventListener('click', function(event) {
    if (!searchInput.contains(event.target)) {
        hintsContainer.innerHTML = '';
        hintsContainer.style.display = 'none';
    }
});
