// Display section

import { useQuery } from "@tanstack/react-query";

import { fetchProperties } from "../api/properties";

export function PropertyList() {
  const { data, isPending, error } = useQuery({
    queryKey: ["properties"],
    queryFn: fetchProperties,
  });

  if (isPending) return <p>Loading properties…</p>;
  if (error) return <p>Could not load properties: {error.message}</p>;
  if (data.length === 0) return <p>No properties yet.</p>;

  return (
    <ul className="property-list">
      {data.map((property) => (
        <li key={property.id} className="property-card">
          <h3>{property.title}</h3>
          <p>{property.city}</p>
          <p className="price">{Number(property.price).toLocaleString("en-IN")}</p>
        </li>
      ))}
    </ul>
  );
}