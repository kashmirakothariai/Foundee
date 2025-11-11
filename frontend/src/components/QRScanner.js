import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Html5QrcodeScanner } from 'html5-qrcode';
import './QRScanner.css';

function QRScanner() {
  const navigate = useNavigate();
  const [scanning, setScanning] = useState(false);

  useEffect(() => {
    if (scanning) {
      const scanner = new Html5QrcodeScanner(
        "qr-reader",
        { 
          fps: 10,
          qrbox: { width: 250, height: 250 }
        },
        false
      );

      scanner.render(onScanSuccess, onScanError);

      function onScanSuccess(decodedText) {
        scanner.clear();
        
        // Get location
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              handleScan(decodedText, position.coords.latitude, position.coords.longitude);
            },
            () => {
              handleScan(decodedText, null, null);
            }
          );
        } else {
          handleScan(decodedText, null, null);
        }
      }

      function onScanError(error) {
        // Ignore errors during scanning
      }

      return () => {
        scanner.clear();
      };
    }
  }, [scanning]);

  const handleScan = (decodedText, lat, lng) => {
    try {
      // Extract QR ID from URL
      const url = new URL(decodedText);
      const pathParts = url.pathname.split('/');
      const qrId = pathParts[pathParts.length - 1];
      
      // Navigate to QR view with location
      navigate(`/qr/${qrId}?lat=${lat}&lng=${lng}`);
    } catch (err) {
      alert('Invalid QR code');
      setScanning(false);
    }
  };

  const handleManualInput = (e) => {
    e.preventDefault();
    const qrId = e.target.qrId.value.trim();
    if (qrId) {
      navigate(`/qr/${qrId}`);
    }
  };

  return (
    <div className="scanner-container">
      <div className="header">
        <div className="header-content">
          <div className="logo">Foundee</div>
          <div className="header-actions">
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/dashboard')}
            >
              Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="card scanner-card">
          <h2>Scan QR Code</h2>
          <p className="scanner-description">
            Scan a Foundee QR code to view contact information and help someone find their lost item.
          </p>

          {!scanning ? (
            <div>
              <button 
                className="btn btn-primary btn-large"
                onClick={() => setScanning(true)}
              >
                Start Scanning
              </button>

              <div className="divider">OR</div>

              <form onSubmit={handleManualInput} className="manual-input">
                <input
                  type="text"
                  name="qrId"
                  placeholder="Enter QR Code ID manually"
                  className="manual-input-field"
                />
                <button type="submit" className="btn btn-secondary">
                  Submit
                </button>
              </form>
            </div>
          ) : (
            <div>
              <div id="qr-reader"></div>
              <button 
                className="btn btn-secondary"
                onClick={() => setScanning(false)}
              >
                Cancel Scanning
              </button>
            </div>
          )}
        </div>

        <div className="card info-card">
          <h3>How it works</h3>
          <ol>
            <li>Click "Start Scanning" and allow camera access</li>
            <li>Point your camera at the QR code</li>
            <li>View the owner's contact information</li>
            <li>Help them recover their lost item!</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default QRScanner;

