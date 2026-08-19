import "./UpdateStatusModal.css";
import { useEffect, useState } from "react";
// import { addStatusEvent } from "../../api/applications";
const { useApplicationsApi } = '../../hooks/useApplicationsApi';



export default function UpdateStatusModal({
    selectedApplication,
    onSuccess,
    onCancel,
}) {
    const [selectedValue, setSelectedValue] = useState("");
        const { addStatusEvent } = useApplicationsApi();

    useEffect(() => {
        setSelectedValue(selectedApplication?.current_status ?? "");
    }, [selectedApplication]);

    function handleChange(event) {
        setSelectedValue(event.target.value);
    }

    async function handleSave() {
        try {
            await addStatusEvent(
                selectedApplication.id,
                selectedValue
            );

            onSuccess?.();
        } catch (error) {
            console.error("Failed to update application status:", error);
        }
    }

    return (
        <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
            <label>
                Update status for{" "}
                <strong>{selectedApplication.company_name}</strong>
            </label>

            <br />
            <br />

            <select
                value={selectedValue}
                onChange={handleChange}
            >
                <option value="Interview">Interview</option>
                <option value="Offer">Offer</option>
                <option value="Rejected">Rejected</option>
                <option value="Withdrawn">Withdrawn</option>
                <option value="Ghosted">Ghosted</option>
            </select>

            <br />
            <br />

            <button onClick={handleSave}>
                Save
            </button>

            <button onClick={onCancel}>
                Cancel
            </button>
        </div>
    );
}