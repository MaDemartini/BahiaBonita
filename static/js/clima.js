document.addEventListener("DOMContentLoaded", function () {
  const API_KEY = '2d8aadf3fd776860d6ede68faa28b06b';
  const city = 'Concón';

  // 1. Clima actual
  fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&lang=es&appid=${API_KEY}`)
    .then(response => response.json())
    .then(data => {
      const iconUrl = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
      document.getElementById('weather-icon').src = iconUrl;
      document.getElementById('weather-description').textContent = data.weather[0].description;
      document.getElementById('weather-temp').textContent = `${Math.round(data.main.temp)}°C`;
      document.getElementById('temp-min').textContent = `${Math.round(data.main.temp_min)}°C`;
      document.getElementById('temp-max').textContent = `${Math.round(data.main.temp_max)}°C`;
    })
    .catch(error => {
      console.error('Error clima actual:', error);
      document.getElementById('weather-description').textContent = 'Error al cargar el clima';
    });

  // 2. Pronóstico 3 horas (agrupado por día)
  fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&lang=es&appid=${API_KEY}`)
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('weather-container');
      container.innerHTML = '';

      const days = {};
      data.list.forEach(item => {
        const date = new Date(item.dt * 1000);
        const day = date.toLocaleDateString('es-CL', { weekday: 'long' });

        if (!days[day]) {
          days[day] = {
            tempMin: item.main.temp_min,
            tempMax: item.main.temp_max,
            icon: item.weather[0].icon,
            desc: item.weather[0].description
          };
        } else {
          days[day].tempMin = Math.min(days[day].tempMin, item.main.temp_min);
          days[day].tempMax = Math.max(days[day].tempMax, item.main.temp_max);
        }
      });

      Object.entries(days).slice(0, 5).forEach(([dayName, info]) => {
        const card = document.createElement('div');
        card.style.border = '1px solid #ccc';
        card.style.borderRadius = '6px';
        card.style.padding = '10px';
        card.style.flex = '1 0 120px';
        card.style.textAlign = 'center';

        card.innerHTML = `
          <h4>${dayName}</h4>
          <img src="https://openweathermap.org/img/wn/${info.icon}@2x.png" style="width:50px;" alt="${info.desc}">
          <p style="text-transform:capitalize;">${info.desc}</p>
          <p>${Math.round(info.tempMax)}°C / ${Math.round(info.tempMin)}°C</p>
        `;
        container.appendChild(card);
      });
    })
    .catch(error => {
      console.error('Error pronóstico:', error);
      document.getElementById('weather-container').textContent = 'Error al cargar el pronóstico.';
    });
});
