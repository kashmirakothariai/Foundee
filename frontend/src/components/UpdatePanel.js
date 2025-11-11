import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { userAPI, qrAPI } from '../utils/api';
import './UpdatePanel.css';

function UpdatePanel() {
  const { qrId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [userDetails, setUserDetails] = useState({
    first_name: '',
    last_name: '',
    mobile_no: '',
    address: '',
    email_id: '',
    blood_grp: '',
    company_name: '',
    description: ''
  });
  const [permissions, setPermissions] = useState({
    first_name: true,
    last_name: true,
    mobile_no: true,
    address: true,
    email_id: true,
    blood_grp: true,
    company_name: true,
    description: true
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isClaiming, setIsClaiming] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login', { state: { from: `/update/${qrId}?bind=${searchParams.get('bind')}` }});
      return;
    }
    loadData();
  }, [qrId, navigate]);

  const loadData = async () => {
    try {
      // Check if we need to bind this QR first
      const shouldBind = searchParams.get('bind') === 'true';
      
      if (shouldBind) {
        setIsClaiming(true);
        try {
          // Bind the QR to current user
          await qrAPI.bindQR(qrId);
          setSuccess('🎉 QR Code claimed successfully! Now add your details.');
        } catch (bindErr) {
          if (bindErr.response?.status === 400) {
            // Already bound, that's okay
            setError('This QR is already claimed. Loading your details...');
          } else {
            throw bindErr;
          }
        }
        setIsClaiming(false);
      }
      
      const [detailsResponse, qrResponse] = await Promise.all([
        userAPI.getDetails(),
        qrAPI.getQRDetails(qrId)
      ]);
      
      setUserDetails(detailsResponse.data);
      
      // Set permissions from QR details
      const qr = qrResponse.data;
      setPermissions({
        first_name: qr.first_name,
        last_name: qr.last_name,
        mobile_no: qr.mobile_no,
        address: qr.address,
        email_id: qr.email_id,
        blood_grp: qr.blood_grp,
        company_name: qr.company_name,
        description: qr.description
      });
    } catch (err) {
      setError('Failed to load data. Make sure you own this QR code.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDetailChange = (field, value) => {
    setUserDetails({ ...userDetails, [field]: value });
  };

  const handlePermissionChange = (field, value) => {
    setPermissions({ ...permissions, [field]: value });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      // Update user details
      await userAPI.updateDetails(userDetails);
      
      // Update QR permissions
      await qrAPI.updatePermissions(qrId, permissions);
      
      setSuccess('Details and permissions updated successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to save changes. Please try again.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading || isClaiming) {
    return <div className="loading">
      {isClaiming ? 'Claiming QR Code...' : 'Loading...'}
    </div>;
  }

  return (
    <div>
      <div className="header">
        <div className="header-content">
          <div className="logo">Foundee</div>
          <div className="header-actions">
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/dashboard')}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="card update-panel">
          <h2>Update QR Details & Permissions</h2>
          <p className="update-subtitle">
            Edit your information and control what others can see when they scan your QR code
          </p>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <form onSubmit={handleSave}>
            <div className="form-sections">
              <div className="form-section">
                <h3>Your Information</h3>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>First Name</label>
                    <input
                      type="text"
                      value={userDetails.first_name || ''}
                      onChange={(e) => handleDetailChange('first_name', e.target.value)}
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.first_name ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('first_name', !permissions.first_name)}
                      title={permissions.first_name ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.first_name ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.first_name ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Last Name</label>
                    <input
                      type="text"
                      value={userDetails.last_name || ''}
                      onChange={(e) => handleDetailChange('last_name', e.target.value)}
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.last_name ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('last_name', !permissions.last_name)}
                      title={permissions.last_name ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.last_name ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.last_name ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Mobile Number</label>
                    <input
                      type="tel"
                      value={userDetails.mobile_no || ''}
                      onChange={(e) => handleDetailChange('mobile_no', e.target.value)}
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.mobile_no ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('mobile_no', !permissions.mobile_no)}
                      title={permissions.mobile_no ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.mobile_no ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.mobile_no ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Email</label>
                    <input
                      type="email"
                      value={userDetails.email_id || ''}
                      onChange={(e) => handleDetailChange('email_id', e.target.value)}
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.email_id ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('email_id', !permissions.email_id)}
                      title={permissions.email_id ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.email_id ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.email_id ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Address</label>
                    <textarea
                      value={userDetails.address || ''}
                      onChange={(e) => handleDetailChange('address', e.target.value)}
                      rows="3"
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.address ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('address', !permissions.address)}
                      title={permissions.address ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.address ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.address ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Blood Group</label>
                    <input
                      type="text"
                      value={userDetails.blood_grp || ''}
                      onChange={(e) => handleDetailChange('blood_grp', e.target.value)}
                      placeholder="e.g., A+, B-, O+"
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.blood_grp ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('blood_grp', !permissions.blood_grp)}
                      title={permissions.blood_grp ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.blood_grp ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.blood_grp ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Company Name</label>
                    <input
                      type="text"
                      value={userDetails.company_name || ''}
                      onChange={(e) => handleDetailChange('company_name', e.target.value)}
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.company_name ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('company_name', !permissions.company_name)}
                      title={permissions.company_name ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.company_name ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.company_name ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Additional Information</label>
                    <textarea
                      value={userDetails.description || ''}
                      onChange={(e) => handleDetailChange('description', e.target.value)}
                      rows="4"
                      placeholder="Any additional information you'd like to share..."
                    />
                  </div>
                  <div className="permission-toggle">
                    <button
                      type="button"
                      className={`visibility-btn ${permissions.description ? 'visible' : 'hidden'}`}
                      onClick={() => handlePermissionChange('description', !permissions.description)}
                      title={permissions.description ? 'Click to hide' : 'Click to show'}
                    >
                      {permissions.description ? (
                        <span className="eye-icon">👁️</span>
                      ) : (
                        <span className="eye-icon eye-closed">👁️‍🗨️</span>
                      )}
                      <span className="visibility-text">
                        {permissions.description ? 'Visible' : 'Hidden'}
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => navigate('/dashboard')}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>

          <div className="info-box">
            <h4>ℹ️ About Permissions</h4>
            <p>
              Use the eye icons to control which information is visible when someone scans your QR code.
              You can change these settings anytime without affecting your stored data.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UpdatePanel;

