import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { qrAPI } from '../utils/api';
import './QRView.css';

function QRView() {
  const { qrId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [qrData, setQrData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadQRData();
  }, [qrId]);

  const loadQRData = async () => {
    try {
      const lat = searchParams.get('lat');
      const lng = searchParams.get('lng');
      
      const response = await qrAPI.scanQR(qrId, lat, lng);
      setQrData(response.data);

      // If user is owner, redirect to update panel
      if (response.data.is_owner) {
        navigate(`/update/${qrId}`);
      }
    } catch (err) {
      setError('Failed to load QR code information');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading QR information...</div>;
  }

  if (error) {
    return (
      <div className="container">
        <div className="card">
          <div className="error-message">{error}</div>
          <button className="btn btn-primary" onClick={() => navigate('/scan')}>
            Scan Another QR
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="header">
        <div className="header-content">
          <div className="logo">Foundee</div>
          <div className="header-actions">
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/scan')}
            >
              Scan Another
            </button>
          </div>
        </div>
      </div>

      <div className="container">
        {!qrData?.user_dtls_id ? (
          <div className="card unbound-card">
            <h2>🎉 Unclaimed QR Code</h2>
            <p>This QR code hasn't been claimed yet. Be the first to claim it!</p>
            <p className="info-text">
              By claiming this QR code, you can attach your contact information so 
              if someone finds your item, they can easily return it to you.
            </p>
            <button 
              className="btn btn-primary"
              onClick={() => {
                const token = localStorage.getItem('token');
                if (token) {
                  // Already logged in, go to bind and edit
                  navigate(`/update/${qrId}?bind=true`);
                } else {
                  // Not logged in, redirect to login first
                  navigate('/login', { state: { from: `/update/${qrId}?bind=true` }});
                }
              }}
            >
              Claim This QR Code
            </button>
            <p className="small-text">You'll need to login with Google to claim this QR</p>
          </div>
        ) : (
          <div className="card contact-card">
            <h2>Contact Information</h2>
            <p className="contact-subtitle">
              Please help return the lost item to its owner
            </p>

            {qrData.user_details ? (
              <div className="contact-details">
                {qrData.user_details.first_name && (
                  <div className="detail-item">
                    <span className="detail-label">First Name:</span>
                    <span className="detail-value">{qrData.user_details.first_name}</span>
                  </div>
                )}
                {qrData.user_details.last_name && (
                  <div className="detail-item">
                    <span className="detail-label">Last Name:</span>
                    <span className="detail-value">{qrData.user_details.last_name}</span>
                  </div>
                )}
                {qrData.user_details.mobile_no && (
                  <div className="detail-item">
                    <span className="detail-label">Mobile:</span>
                    <span className="detail-value">
                      <a href={`tel:${qrData.user_details.mobile_no}`}>
                        {qrData.user_details.mobile_no}
                      </a>
                    </span>
                  </div>
                )}
                {qrData.user_details.email_id && (
                  <div className="detail-item">
                    <span className="detail-label">Email:</span>
                    <span className="detail-value">
                      <a href={`mailto:${qrData.user_details.email_id}`}>
                        {qrData.user_details.email_id}
                      </a>
                    </span>
                  </div>
                )}
                {qrData.user_details.address && (
                  <div className="detail-item">
                    <span className="detail-label">Address:</span>
                    <span className="detail-value">{qrData.user_details.address}</span>
                  </div>
                )}
                {qrData.user_details.blood_grp && (
                  <div className="detail-item">
                    <span className="detail-label">Blood Group:</span>
                    <span className="detail-value">{qrData.user_details.blood_grp}</span>
                  </div>
                )}
                {qrData.user_details.company_name && (
                  <div className="detail-item">
                    <span className="detail-label">Company:</span>
                    <span className="detail-value">{qrData.user_details.company_name}</span>
                  </div>
                )}
                {qrData.user_details.description && (
                  <div className="detail-item">
                    <span className="detail-label">Additional Info:</span>
                    <span className="detail-value">{qrData.user_details.description}</span>
                  </div>
                )}
              </div>
            ) : (
              <p>No contact information available.</p>
            )}

            <div className="alert-info">
              <p>📧 The owner has been notified via email with your location.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default QRView;

