import { useAuth } from "react-oidc-context";

export function useAuthenticatedFetch() {
    const auth = useAuth();
    const token = auth.user?.access_token;

    async function apiFetch(url, options = {}) {
        return fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`,
            },
        });
    }

    return apiFetch;
}