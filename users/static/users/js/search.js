function searchJobs() {
    const query = document.getElementById('search-input').value.trim();
    const industry = document.getElementById('industry-filter').value;
    const city = document.getElementById('city-filter').value;

    let params = `?q=${encodeURIComponent(query)}`;
    if (industry) {
        params += `&industry=${encodeURIComponent(industry)}`;
    }
    if (city) {
        params += `&city=${encodeURIComponent(city)}`;
    }

    fetch(`/jobs/api/jobs/search/${params}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => { 
          // console.log(data);
          renderVacancies(data) 
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(`Произошла ошибка: ${error.message}`);
        });
}

document.getElementById('search-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        searchJobs();
    }
});