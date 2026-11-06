// talking to backend

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export interface Property {
  id: number;
  title: string;
  city: string;
  price: string;
  created_at: string;
}

export async function fetchProperties(): Promise<Property[]> {
  const response = await fetch(`${API_URL}/properties`);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}