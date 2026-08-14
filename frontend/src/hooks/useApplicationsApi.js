import { useAuthenticatedFetch } from "./useAuthenticatedFetch";

const BASE_URL = "http://localhost:8000"; // TODO: update to env var before deployment

export function useApplicationsApi() {
    const authedFetch = useAuthenticatedFetch();

    const fetchApplications = async () => {
      const response = await authedFetch(`${BASE_URL}/applications`);
    
      if (!response.ok) {
        throw new Error(`Failed to fetch applications. Status: ${response.status}`);
      }
    
      return response.json();
    };

    const createApplication = async (payload) => {
      const response = await authedFetch(`${BASE_URL}/applications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
    
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    
      return response.json();
    };

    const addStatusEvent = async (applicationId, status) => {
      const response = await authedFetch(`${BASE_URL}/applications/${applicationId}/status_events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });
    
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    
      return response.json();
    };

    return {
        fetchApplications,
        createApplication,
        addStatusEvent
    }
}