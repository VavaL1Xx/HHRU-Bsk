function fetchData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка при получении данных с ${url}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error(`Ошибка: ${error.message}`);
            return [];
        });
}

async function loadAllData(url) {
    try {
        const jobs = await fetchData(url);
        renderVacancies(jobs);
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
    }
}

function renderVacancies(jobs = []) {
  const vacancyList = document.getElementById('vacancy-list-ul');
  vacancyList.innerHTML = '';
  // console.log(jobs);
  if (!jobs || jobs.length === 0) {
      vacancyList.innerHTML = `
      <li>
        <div class="vacancy-item empty-list">
          <h4>Вакансии отсутствуют</h4>
        </div>
      </li>`;
      return;
  }

  quantity = document.getElementById("search-results");
  quantity.innerHTML = `Найденно ${jobs.length} вакансий`;

  jobs.forEach(job => {
    const profilePicture = job['employer']['user']['profile_picture'] || "/static/users/images/user_avatar_default.png";
    const jobElement = document.createElement('li');
    jobElement.innerHTML = `
        <div class="vacancy-item">
          <div class="vacancy-main-info">
            <div class="main-side">
              <div class="vacancy-image">
                <img src="${profilePicture}" alt="${job['employer']['company_name']} логотип" class="company-logo">
              </div>
              <div>
                <p class="item-date">${new Date(job['date_of_creation']).toLocaleString()}</p>
                <h4>${ job['title'] }</h4>
                <p class="company">${ job['employer']['company_name'] }</p>
              </div>
            </div>
            <div class="vacancy-side-info">
              <span>${ job['resps'] } откликов</span>
            </div>
          </div>
          <p class="description" style="margin-bottom:0;display:flex;gap:12px;"><span class="alt-info">${ job['location'] }</span></p>
          <p class="salary">${ job['salary'] }</p>
          <p class="description">${ job['description'] }</p>
          <p class="description">${ job['requirements'] }</p>
          <div class="job-btns-container">
            <div class="btns-block" id="btns-block-${job['id']}">
            </div>
          </div>
        </div>
    `;
    vacancyList.appendChild(jobElement);
    
    const btns_lst = document.getElementById(`btns-block-${job['id']}`);
    
    if (!isSuper && isAuthenticated){ 
      if (featuredJobs && !featuredJobs.includes(job['id'])){
        btns_lst.innerHTML += `<a class="btn learn-more" href="/jobs/create/feature/${job['id']}"><i class="fi fi-ss-heart"></i></a>`
      }
      else {
        btns_lst.innerHTML += `<a class="btn learn-more featured" href="/jobs/delete/feature/${job['id']}"><i class="fi fi-ss-heart"></i></a>`
      }
    }

    btns_lst.innerHTML += `<a class="btn learn-more" href="jobs/view/job/${job['id']}/">Подробнее</a>`
    
    if (!isSuper && isAuthenticated){
      if (userType == 'seeker'){
        if (respondedJobs.includes(job['id'])){
          btns_lst.innerHTML += `<span class="btn btn-invert responded">Вы откликнулись</span>`
        }
        else{
          btns_lst.innerHTML += `<a class="btn btn-invert" href="/jobs/create/response/${job['id']}">Откликнуться</a>`
        }
      }
      if (userType == 'employer' && userId == job['employer']['user']['id']){
        btns_lst.innerHTML += `<a class="btn btn-invert close" href="/jobs/delete/job/${job['id']}">Закрыть</a>`
      }
    }
  });
}
