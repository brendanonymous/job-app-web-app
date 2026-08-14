import './CreateApplicationForm.css';
import { useApplicationsApi } from '../../hooks/useApplicationsApi';
// import { createApplication } from '../../api/applications';

export default function CreateApplicationForm({ onSuccess }) {
    const { createApplication } = useApplicationsApi();

    async function handleSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const payload = {
            company_name: formData.get('company_name')?.toString().trim(),
            role_name: formData.get('role_name')?.toString().trim(),
            applied_date: formData.get('applied_date')?.toString() || null,
        };

        if (!payload.company_name || !payload.role_name) {
            return;
        }

        try {
            await createApplication(payload);
            form.reset();
            onSuccess?.();
        } catch (error) {
            console.error('Failed to create application:', error);
        }
    }

    return (
        <form method="post" onSubmit={handleSubmit}>
            <label>
                Company: <input name="company_name" />
            </label>
            <hr />
            <label>
                Role: <input name="role_name" />
            </label>
            <hr />
            <label>
                Date Applied: <input name="applied_date" type="date" />
            </label>
            <hr />
            <button type="submit">Submit</button>
        </form>
    );
}