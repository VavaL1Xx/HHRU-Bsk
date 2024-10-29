function searchJobs(url, extract = false, query = null, industry = null, city = null) {

    if (query){
        query = query;
    }
    else{
        query = document.getElementById('search-input').value.trim();
    }

    if (industry){
        industry = industry
    }
    else{
        industry = document.getElementById('industry-filter').value;
    }

    if (city){
        city = city
    }
    else{
        city = document.getElementById('city-filter').value;
    }

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
          renderVacancies(data, extract) 
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(`Произошла ошибка: ${error.message}`);
        });
}