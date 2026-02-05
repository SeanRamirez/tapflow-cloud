import React, { useState, useEffect } from 'react';
// 👇 This must be two dots (..) to go up one folder to find 'api'
import { api } from '../api/client';

function SalesCard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getSalesSummary()
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching sales data:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-4">Loading metrics...</div>;
  if (!data) return <div className="p-4">No data available</div>;

  // Simple inline styles for a clean look
  const cardStyle = {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '20px',
    margin: '10px',
    backgroundColor: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  };

  return (
    <div style={cardStyle}>
      <h2 style={{ marginTop: 0, color: '#333' }}>Real-Time Sales</h2>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '15px' }}>
        <div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2ecc71' }}>
            {data.total_pints}
          </div>
          <div style={{ color: '#666' }}>Pints Sold</div>
        </div>
        <div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3498db' }}>
            ${data.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
          <div style={{ color: '#666' }}>Total Revenue</div>
        </div>
        <div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#9b59b6' }}>
            ${data.avg_price.toFixed(2)}
          </div>
          <div style={{ color: '#666' }}>Avg Price</div>
        </div>
      </div>
    </div>
  );
}

export default SalesCard;