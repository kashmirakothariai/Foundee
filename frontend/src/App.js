import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import QRScanner from './components/QRScanner';
import QRView from './components/QRView';
import UpdatePanel from './components/UpdatePanel';
import './App.css';

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;

function App() {
  // Detailed environment debugging
  console.log('=== REACT ENVIRONMENT VARIABLE DEBUG ===');
  console.log('🔍 NODE_ENV:', process.env.NODE_ENV);
  console.log('🔍 GOOGLE_CLIENT_ID from env:', process.env.REACT_APP_GOOGLE_CLIENT_ID);
  console.log('🔍 GOOGLE_CLIENT_ID variable:', GOOGLE_CLIENT_ID);
  console.log('🔍 Type:', typeof GOOGLE_CLIENT_ID);
  
  // Show all REACT_APP variables
  const reactAppVars = Object.keys(process.env).filter(k => k.startsWith('REACT_APP'));
  console.log('🔍 All REACT_APP variables found:', reactAppVars);
  
  // Show which .env file is being used
  console.log('=== 📁 WHICH .ENV FILE IS REACT USING? ===');
  console.log('🏷️  ENV_SOURCE identifier:', process.env.REACT_APP_ENV_SOURCE);
  
  if (process.env.REACT_APP_ENV_SOURCE === 'env_local_file') {
    console.log('✅ React is reading from: .env.local (HIGH PRIORITY)');
  } else if (process.env.REACT_APP_ENV_SOURCE === 'env_development_file') {
    console.log('✅ React is reading from: .env.development (MEDIUM PRIORITY)');
  } else if (process.env.REACT_APP_ENV_SOURCE === 'env_file') {
    console.log('✅ React is reading from: .env (LOW PRIORITY)');
  } else {
    console.log('❓ Unknown source - check your .env files');
  }
  
  console.log('=== 📋 REACT .ENV FILE PRIORITY ORDER ===');
  console.log('1️⃣  .env.development.local (HIGHEST - overrides all)');
  console.log('2️⃣  .env.local (HIGH - overrides development & base)');
  console.log('3️⃣  .env.development (MEDIUM - overrides base only)');
  console.log('4️⃣  .env (LOWEST - used if others don\'t have the variable)');
  console.log('===========================================');
  
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/scan" element={<QRScanner />} />
            <Route path="/qr/:qrId" element={<QRView />} />
            <Route path="/update/:qrId" element={<UpdatePanel />} />
            <Route path="/" element={<Navigate to="/scan" />} />
          </Routes>
        </div>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;

