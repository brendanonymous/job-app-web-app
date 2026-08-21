import "./ApplicationsTable.css"
import { useState, useEffect } from "react"
import { useApplicationsApi } from '../../hooks/useApplicationsApi';

export default function ApplicationsTable({ refreshTrigger = 0,  onApplicationSelected}) {
    const [applications, setApplications] = useState([]);
    const { fetchApplications } = useApplicationsApi();
    
    async function loadApplications() {
        const data = await fetchApplications();
        setApplications(data);
    }

    useEffect(() => {
        loadApplications();
    }, [refreshTrigger]);
    
    const listOfApplications = applications.map(application => (
        <tr key={application.id} onClick={() => onApplicationSelected(application)}>
            <td>{application.company_name}</td>
            <td>{application.role_name}</td>
            <td>{application.applied_date}</td>
            <td>{application?.current_status}</td>
        </tr>
    ));

    return (
        <table>
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Date Applied</th>
                    <th>Current Status</th>
                </tr>
            </thead>
            <tbody>
                {listOfApplications}
            </tbody>
        </table>
    );
}