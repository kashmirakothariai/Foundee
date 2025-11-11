import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { authAPI } from '../utils/api';
import './Login.css';

function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState('');

  useEffect(() => {
    // If already logged in, redirect
    if (localStorage.getItem('token')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleGoogleSuccess = async (credentialResponse) => {
    console.log('🔥 Google OAuth Success - got credential:', credentialResponse);
    try {
      console.log('📡 Sending request to backend...');
      const response = await authAPI.googleLogin(credentialResponse.credential);
      console.log('✅ Backend response:', response);
      
      localStorage.setItem('token', response.data.access_token);
      
      // Redirect to original destination or dashboard
      const from = location.state?.from || '/dashboard';
      navigate(from);
    } catch (err) {
      console.error('❌ Backend connection failed:', err);
      console.error('❌ Error details:', err.response?.data || err.message);
      setError('Failed to login with Google. Please try again.');
    }
  };

  const handleGoogleError = () => {
    setError('Google login failed. Please try again.');
  };

  return (
    <div className="login-container">
      <div className="login-card card">
        <div className="login-header">
          <h1 className="login-logo">Foundee</h1>
          <p className="login-subtitle">QR-based Lost and Found</p>
          <p className="login-owner">By Gaurang Kothari (X Googler)</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="login-content">
          <h2>Sign in to continue</h2>
          <p className="login-description">
            Login is required to edit your QR details or register new QR codes
          </p>

          <div className="google-login-wrapper">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              useOneTap={false}
              auto_select={false}
              theme="filled_blue"
              size="large"
              text="signin_with"
              shape="rectangular"
              type="standard"
              width="300"
            />
          </div>

          <div className="login-divider">
            <span>OR</span>
          </div>

          <button 
            className="btn btn-secondary btn-full"
            onClick={() => navigate('/scan')}
          >
            Continue without login (Scan QR only)
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;

