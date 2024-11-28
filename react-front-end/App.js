import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [seriesId, setSeriesId] = useState('');
  const [startDate, setStartDate] = useState('2000-01-01');
  const [endDate, setEndDate] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [image, setImage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      series_id: seriesId,
      start_date: startDate || null,
      end_date: endDate || null,
      api_key: apiKey,
    };

    axios.post('http://localhost:5000/api/get_chart', payload)
      .then(response => {
        setImage(`data:image/png;base64,${response.data.image}`);
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  };

  return (
    <div className="App">
      <h1>FRED Data Fetcher</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Series ID:</label>
          <input type="text" value={seriesId} onChange={(e) => setSeriesId(e.target.value)} required />
        </div>
        <div>
          <label>Start Date (YYYY-MM-DD):</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>
        <div>
          <label>End Date (YYYY-MM-DD):</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
        <div>
          <label>API Key:</label>
          <input type="text" value={apiKey} onChange={(e) => setApiKey(e.target.value)} required />
        </div>
        <button type="submit">Fetch and Plot</button>
      </form>
      {image && <img src={image} alt="FRED Data Chart" />}
    </div>
  );
}

export default App;
