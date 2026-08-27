import './App.css';
import { useState } from 'react';
import { useAuth } from "react-oidc-context";

import PopUp from './components/PopUp/PopUp';
import ApplicationsTable from './components/ApplicationsTable/ApplicationsTable';
import CreateApplicationForm from './components/CreateApplicationForm/CreateApplicationForm';
import UpdateStatusModal from './components/UpdateStatusModal/UpdateStatusModal';
import SankeyModal from './components/SankeyModal/SankeyModal';

function App() {
  const [activeModal, setActiveModal] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [selectedApplication, setSelectedApplication] = useState(null);
  const auth = useAuth();
  
  const handleSignout = async () => {
    await auth.removeUser();

    const clientId = "31o3ue4c6mdqqftjuvogtqdm13";
    const logoutUri = "http://localhost:5173/";
    const cognitoDomain =
      "https://us-east-1izktuwo0g.auth.us-east-1.amazoncognito.com";

    window.location.assign(
      `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`
    );
  };

  const openModal = (modal) => {
    setActiveModal(modal);
  };

  const closeModal = () => {
    setActiveModal(null);
    setSelectedApplication(null);
  };

  const handleApplicationUpdated = () => {
    setActiveModal(null);
    setSelectedApplication(null);
    setRefreshKey((prev) => prev + 1);
  };

  const handleApplicationCreated = () => {
    setActiveModal(null);
    setRefreshKey((prev) => prev + 1);
  };

  const handleApplicationSelected = (application) => {
    setSelectedApplication(application);
    setActiveModal('update');
  };

  return (
    <>
      <h1>JobFlow</h1>

      {/* GENERATE SANKEY CHART */}
      <button onClick={() => openModal('sankey')}>
        Generate Sankey Chart
      </button>
      <PopUp
        showPopUp={activeModal === 'sankey'}
        closePopUp={closeModal}>
        <SankeyModal/>
      </PopUp>

      {/* ADD APPLICATION */}
      <button onClick={() => openModal('create')}>
        Add New Application
      </button>
      <PopUp
        showPopUp={activeModal === 'create'}
        closePopUp={closeModal}>
        <CreateApplicationForm
          onSuccess={handleApplicationCreated}/>
      </PopUp>

      {/* UPDATE APPLICATION STATUS */}
      <PopUp
        showPopUp={activeModal === 'update'}
        closePopUp={closeModal}>
        <UpdateStatusModal
          selectedApplication={selectedApplication}
          onSuccess={handleApplicationUpdated}/>
      </PopUp>

      {/* LIST OF APPLICATIONS */}
      <ApplicationsTable
        refreshTrigger={refreshKey}
        onApplicationSelected={handleApplicationSelected}
      />

      {/* SIGN OUT */}
      <button onClick={handleSignout}>
        Sign out
      </button>
    </>
  );
}

export default App;