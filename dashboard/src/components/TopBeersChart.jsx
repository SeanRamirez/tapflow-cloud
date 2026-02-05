import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
// 👇 This must also be two dots (..)
import { api } from '../api/client';

function TopBeersChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.getTopBeers(5)
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ 
      border: '1px solid #ddd', 
      borderRadius: '8px', 
      padding: '20px', 
      margin: '10px', 
      backgroundColor: 'white' 
    }}>
      <h3 style={{ marginTop: 0 }}>Top 5 Beers by Revenue</h3>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="beer_name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="total_revenue" fill="#8884d8" name="Revenue ($)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default TopBeersChart;
