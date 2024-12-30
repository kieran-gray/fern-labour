import { useAuth } from 'react-oidc-context';
import React, { useEffect, useState } from 'react';
import { BirthingPersonService, BirthingPersonDTO } from "../../client"
import { OpenAPI } from '../../client/sdk.gen';

const getBirthingPerson = async () => {
  return await BirthingPersonService.getBirthingPersonApiV1BirthingPersonGet()
}

export const BirthingPerson: React.FC = () => {
  const auth = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your actual endpoint method
        const token = auth.user?.access_token;
        OpenAPI.headers = {
          'Authorization': `Bearer ${token}`
        }

        const response = await BirthingPersonService.getBirthingPersonApiV1BirthingPersonGet();
        setData(response.birthing_person);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data found</div>;

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>An error occurred</div>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Data from API</h2>
      <pre className="bg-gray-100 p-4 rounded">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
};
