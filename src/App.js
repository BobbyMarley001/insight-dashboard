import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie, Line } from 'react-chartjs-2';
import 'chart.js/auto';

function App() {
  const [topic, setTopic] = useState('');
  const [country, setCountry] = useState('');
  const [region, setRegion] = useState('');
  const [year, setYear] = useState('');
  const [topics, setTopics] = useState([]);
  const [countries, setCountries] = useState([]);
  const [regions, setRegions] = useState([]);
  const [years, setYears] = useState([]);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load topics, years, regions on page load
  useEffect(() => {
    axios.get('http://localhost:5000/api/topics').then(res => setTopics(res.data));
    axios.get('http://localhost:5000/api/years').then(res => setYears(res.data));
    axios.get('http://localhost:5000/api/regions').then(res => setRegions(res.data));
  }, []);

  // Load countries based on selected topic
  useEffect(() => {
    let url = 'http://localhost:5000/api/countries';
    if (topic) url += `?topic=${encodeURIComponent(topic)}`;
    axios.get(url).then(res => setCountries(res.data));
  }, [topic]);

  // Load insight data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      let url = 'http://localhost:5000/api/data';
      const params = new URLSearchParams();
      if (topic) params.append('topic', topic);
      if (country) params.append('country', country);
      if (region) params.append('region', region);
      if (year) params.append('start_year', year);
      url += '?' + params.toString();

      try {
        const res = await axios.get(url);
        setData(res.data);
      } catch (err) {
        console.error('API fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [topic, country, region, year]);

  // Charts
  const barChartData = {
    labels: data.map(d => d.country || 'Unknown'),
    datasets: [
      {
        label: 'Intensity',
        data: data.map(d => d.intensity || 0),
        backgroundColor: 'rgba(75,192,192,0.6)',
      }
    ]
  };

  const pieChartData = {
    labels: data.map(d => d.region || 'Unknown'),
    datasets: [
      {
        label: 'Region Intensity',
        data: data.map(d => d.intensity || 0),
        backgroundColor: [
          '#f94144', '#f3722c', '#f8961e', '#f9844a',
          '#f9c74f', '#90be6d', '#43aa8b', '#577590'
        ]
      }
    ]
  };

  const lineChartData = {
    labels: [...new Set(data.map(d => d.start_year).filter(Boolean))].sort((a, b) => a - b),
    datasets: [
      {
        label: 'Intensity Trend by Year',
        data: data
          .filter(d => d.start_year)
          .sort((a, b) => a.start_year - b.start_year)
          .map(d => d.intensity || 0),
        borderColor: '#36a2eb',
        tension: 0.4,
        fill: false
      }
    ]
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f4f4', minHeight: '100vh' }}>
      <h2 style={{ textAlign: 'center' }}>🌍 Global Insights Dashboard</h2>

      {/* Filter Section */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1rem',
        marginBottom: '2rem',
        justifyContent: 'center'
      }}>
        <Dropdown label="Topic" value={topic} onChange={setTopic} options={topics} />
        <Dropdown label="Country" value={country} onChange={setCountry} options={countries} />
        <Dropdown label="Region" value={region} onChange={setRegion} options={regions} />
        <Dropdown label="Start Year" value={year} onChange={setYear} options={years} />
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Loading data...</p>}

      {!loading && data.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '2rem',
          padding: '1rem'
        }}>
          <ChartCard title="Intensity by Country">
            <Bar data={barChartData} />
          </ChartCard>
          <ChartCard title="Intensity by Region">
            <Pie data={pieChartData} />
          </ChartCard>
          <ChartCard title="Trend Over Years" full>
            <Line data={lineChartData} />
          </ChartCard>
        </div>
      )}

      {!loading && data.length === 0 && (
        <p style={{ textAlign: 'center', color: 'gray' }}>No data found for selected filters.</p>
      )}
    </div>
  );
}

// 🔧 Helper component for filters
const Dropdown = ({ label, value, onChange, options }) => (
  <div>
    <label><strong>{label}:</strong></label><br />
    <select value={value} onChange={e => onChange(e.target.value)}>
      <option value="">All</option>
      {options.map((opt, i) => <option key={i} value={opt}>{opt}</option>)}
    </select>
  </div>
);

// 📦 Chart wrapper
const ChartCard = ({ title, children, full }) => (
  <div style={{
    background: '#fff',
    padding: '1rem',
    borderRadius: '8px',
    gridColumn: full ? 'span 2' : 'auto'
  }}>
    <h4 style={{ textAlign: 'center' }}>{title}</h4>
    {children}
  </div>
);

export default App;

