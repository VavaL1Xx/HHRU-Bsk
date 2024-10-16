function searchJobs(url, extract = false) {

    const query = document.getElementById('search-input').value.trim();
    const industry = document.getElementById('industry-filter').value;
    const city = document.getElementById('city-filter').value;

    console.log(query);
    console.log(industry);
    console.log(city);

    let params = `?q=${encodeURIComponent(query)}`;
    if (industry) {
        params += `&industry=${encodeURIComponent(industry)}`;
    }
    if (city) {
        params += `&city=${encodeURIComponent(city)}`;
    }

    fetch(`${url}${params}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => { 
          // console.log(data);
          renderVacancies(data, extract) 
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(`Произошла ошибка: ${error.message}`);
        });
}