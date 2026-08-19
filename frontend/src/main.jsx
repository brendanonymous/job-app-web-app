import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AuthProvider } from "react-oidc-context";
import './index.css'
import AuthedApp from './components/AuthedApp/AuthedApp.jsx';

const cognitoAuthConfig = {
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_izKTUwo0G",
  client_id: "31o3ue4c6mdqqftjuvogtqdm13",
  redirect_uri: "http://localhost:5173/callback",
  response_type: "code",
  scope: "phone openid email",
};

createRoot(document.getElementById('root')).render(
  <AuthProvider {...cognitoAuthConfig}>
    <AuthedApp />
  </AuthProvider>
);
