

export function useAnalyticsApi() {
    const fetchSankeyData = async () => {
        const response = await fetch(`${BASE_URL}/analytics/sankey`);

        if (!response.ok) {
            throw new Error(`Failed to fetch Sankey data. Status: ${response.status}`);
        }

        return response.json();
    };

    return {
        fetchSankeyData
    }
}
