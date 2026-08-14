import './SankeyModal.css'
import { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
// import { fetchSankeyData } from '../../api/analytics';
import { useAnalyticsApi } from '../../hooks/useAnalyticsApi';

export default function SankeyModal() {
    const [sankeyData, setSankeyData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { fetchSankeyData } = useAnalyticsApi();

    const labels = [
        'Applied',
        'Interview 1',
        'Interview 2',
        'Interview 3',
        'Interview 4',
        'Interview 5',
        'Interview 6',
        'Rejected',
        'Ghosted',
        'Withdrawn',
        'Offer'
    ];

    async function loadSankeyChart() {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchSankeyData();
            setSankeyData(data);
        } catch (e) {
            setError(e.message || 'Failed to load Sankey data');
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadSankeyChart();
    }, []);

    return (
        <div className="sankey-modal">
            <div className="sankey-controls">
                <button type="button" onClick={loadSankeyChart}>Reload</button>
            </div>

            {loading && <div className="sankey-loading">Loading Sankey chart...</div>}
            {error && <div className="sankey-error">{error}</div>}

            {sankeyData && (
                <Plot
                    data={[{
                        type: 'sankey',
                        orientation: 'h',
                        node: {
                            label: labels,
                            pad: 15,
                            thickness: 20,
                            color: 'rgba(200,200,200,0.9)'
                        },
                        link: {
                            source: sankeyData.sources,
                            target: sankeyData.targets,
                            value: sankeyData.values,
                            color: sankeyData.colors
                        }
                    }]}
                    layout={{ title: 'Application Flow', font: { size: 12 }, height: 520 }}
                    config={{ responsive: true }}
                />
            )}
        </div>
    );
}