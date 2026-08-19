import { useAuthenticatedFetch } from "./useAuthenticatedFetch";

const BASE_URL = "http://localhost:8000"; // TODO: update to env var before deployment

export function useAnalyticsApi() {
    const authedFetch = useAuthenticatedFetch();

    const fetchSankeyData = async () => {
        const response = await authedFetch(`${BASE_URL}/analytics/sankey`);

        if (!response.ok) {
            throw new Error(`Failed to fetch Sankey data. Status: ${response.status}`);
        }

        return response.json();
    };

    return {
        fetchSankeyData
    }
}
