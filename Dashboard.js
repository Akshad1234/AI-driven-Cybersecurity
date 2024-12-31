import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';

const Dashboard = () => {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/threats')
            .then((response) => {
                const data = response.data;
                setChartData({
                    labels: data.map((item) => item.timestamp),
                    datasets: [{
                        label: 'Threat Level',
                        data: data.map((item) => item.threat_level),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    }],
                });
            })
            .catch((error) => console.error('Error:', error));
    }, []);

    return (
        <div>
            <h2>Threat Dashboard</h2>
            <Bar data={chartData} />
        </div>
    );
};

export default Dashboard;
