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

async function loadAllData(url, extract = false) {
  try {
    const jobs = await fetchData(url);
    renderVacancies(jobs, extract);
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
}

function renderVacancies(data = [], extract = false) {
  const vacancyList = document.getElementById('vacancy-list-ul');
  vacancyList.innerHTML = '';
  // console.log(jobs);

  quantity = document.getElementById("search-results");
  quantity.innerHTML = "";
  const n = data.length;
  word = ""
  // console.log(n);
  if (!n || n > 4 && n < 21 || n % 10 > 4)
    word = "вакансий";
  else if (n % 10 > 1)
    word = "вакансии";
  else
    word = "вакансия";

  plural_modifier = "Найдено";

  if (n == 1)
    plural_modifier = "Найдена";

  quantity.innerHTML = `${plural_modifier} ${n} ${word}...`;

  if (!data || data.length === 0) {
    vacancyList.innerHTML = `
      <li>
        <div class="vacancy-item empty-list">
          <h4>Вакансии отсутствуют</h4>
        </div>
      </li>`;
    return;
  }

  if (extract) {
    data.forEach(job => {
      renderVac(job['job'], vacancyList);
    });
  }
  else {
    data.forEach(job => {
      renderVac(job, vacancyList);
    });
  }
}

function renderVac(job, vacancyList) {
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
                <h4>${job['title']}</h4>
                <p class="company">${job['employer']['company_name']}</p>
              </div>
            </div>
            <div class="vacancy-side-info">
              <span style="display:flex;justify-content:end;width:100%;gap: 8px;"><i class="fi fi-ss-land-layer-location"></i>${job['location']}</span>
              <span style="text-align: right;">${job['resps']} откликов</span>
            </div>
          </div>
          <p class="description" id="skills-${job['id']}" style="margin-bottom:0;display:flex;gap:12px;flex-wrap:wrap;"></p>
          <p class="salary">${job['salary']}</p>
          <p class="description">${job['description']}</p>
          <div class="job-btns-container">
            <div class="btns-block" id="btns-block-${job['id']}">
            </div>
          </div>
        </div>
    `;
  vacancyList.appendChild(jobElement);

  skls = document.getElementById(`skills-${job['id']}`);
  skls.innerHTML = "";

  if (job['skills'] && job['skills'].length > 0) {
    job['skills'].forEach(skill => {
      skls.innerHTML += `<span class="alt-info">${skill.name}</span>`;
    });
  } else {
    skls.innerHTML += `<span class="alt-info">Нет навыков</span>`;
  }
  // <span class="alt-info">${ job['location'] }</span>
  const btns_lst = document.getElementById(`btns-block-${job['id']}`);

  if (!isSuper && isAuthenticated) {
    if (featuredJobs && !featuredJobs.includes(job['id'])) {
      btns_lst.innerHTML += `<a class="btn learn-more" href="/jobs/create/feature/${job['id']}"><i class="fi fi-ss-heart"></i></a>`
    }
    else {
      btns_lst.innerHTML += `<a class="btn learn-more red" href="/jobs/delete/feature/${job['id']}"><i class="fi fi-ss-heart"></i></a>`
    }
  }

  btns_lst.innerHTML += `<a class="btn learn-more" href="jobs/view/job/${job['id']}/">Подробнее</a>`

  if (!isSuper && isAuthenticated) {
    if (userType == 'seeker') {
      if (respondedJobs.includes(job['id'])) {
        btns_lst.innerHTML += `<span class="btn btn-invert green-invert">Вы откликнулись</span>`
      }
      else {
        btns_lst.innerHTML += `<a class="btn btn-invert" href="/jobs/create/response/${job['id']}">Откликнуться</a>`
      }
    }
    if (userType == 'employer' && userId == job['employer']['user']['id']) {
      btns_lst.innerHTML += `<a class="btn btn-invert close" href="/jobs/delete/job/${job['id']}">Закрыть</a>`
    }
  }
}
