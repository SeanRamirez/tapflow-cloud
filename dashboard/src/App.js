import React from 'react';
import SalesCard from './components/SalesCard';
import TopBeersChart from './components/TopBeersChart';

function App() {
  return (
    <div style={{ backgroundColor: '#f5f7fa', minHeight: '100vh', padding: '20px' }}>
      <header style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ color: '#2c3e50' }}>🍺 TapFlow Analytics</h1>
        <p style={{ color: '#7f8c8d' }}>Real-time Brewery Inventory Management</p>
      </header>
      
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <SalesCard />
        <TopBeersChart />
      </div>
    </div>
  );
}

export default App;