import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { userAPI, qrAPI } from '../utils/api';
import QRCode from 'qrcode';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [qrCodes, setQrCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    loadData();
  }, [navigate]);

  const loadData = async () => {
    try {
      const [userResponse, qrResponse] = await Promise.all([
        userAPI.getMe(),
        qrAPI.getMyQRCodes()
      ]);
      setUser(userResponse.data);
      setQrCodes(qrResponse.data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleCreateQR = async () => {
    try {
      const response = await qrAPI.createQR({});
      setQrCodes([...qrCodes, response.data]);
    } catch (err) {
      setError('Failed to create QR code');
      console.error(err);
    }
  };

  const downloadQR = async (qrId) => {
    try {
      const url = `${window.location.origin}/qr/${qrId}`;
      const canvas = await QRCode.toCanvas(url, {
        width: 300,
        margin: 2,
      });
      const link = document.createElement('a');
      link.download = `foundee-qr-${qrId}.png`;
      link.href = canvas.toDataURL();
      link.click();
    } catch (err) {
      console.error('Failed to generate QR code:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div>
      <div className="header">
        <div className="header-content">
          <div className="logo">Foundee</div>
          <div className="header-actions">
            <span className="user-email">{user?.email_id}</span>
            <button className="btn btn-secondary" onClick={() => navigate('/scan')}>
              Scan QR
            </button>
            <button className="btn btn-secondary" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="container">
        {error && <div className="error-message">{error}</div>}

        <div className="card">
          <div className="dashboard-header">
            <h2>My QR Codes</h2>
            <button className="btn btn-primary" onClick={handleCreateQR}>
              Create New QR
            </button>
          </div>

          {qrCodes.length === 0 ? (
            <div className="empty-state">
              <p>You don't have any QR codes yet.</p>
              <button className="btn btn-primary" onClick={handleCreateQR}>
                Create Your First QR
              </button>
            </div>
          ) : (
            <div className="qr-grid">
              {qrCodes.map((qr) => (
                <div key={qr.id} className="qr-card">
                  <div className="qr-preview">
                    <canvas 
                      ref={(canvas) => {
                        if (canvas) {
                          QRCode.toCanvas(
                            canvas,
                            `${window.location.origin}/qr/${qr.id}`,
                            { width: 200, margin: 2 }
                          );
                        }
                      }}
                    />
                  </div>
                  <div className="qr-actions">
                    <button 
                      className="btn btn-secondary btn-small"
                      onClick={() => navigate(`/update/${qr.id}`)}
                    >
                      Edit Details
                    </button>
                    <button 
                      className="btn btn-primary btn-small"
                      onClick={() => downloadQR(qr.id)}
                    >
                      Download
                    </button>
                  </div>
                  <div className="qr-id">ID: {qr.id}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card">
          <h2>Quick Actions</h2>
          <div className="action-buttons">
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/update/' + (qrCodes[0]?.id || 'new'))}
            >
              Update My Details
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/scan')}
            >
              Scan a QR Code
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

