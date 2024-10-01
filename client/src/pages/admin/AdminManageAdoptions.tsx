import AdminNavBar from "./AdminNavbar.tsx";
import { useEffect, useState } from "react";
import Loader from "../general/Loader.tsx";

function AdminManageAdoptionsPage() {
  const [adoptions, setAdoptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAdoptions();
  }, []);

  const fetchAdoptions = async () => {
    try {
      setLoading(true);
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/getAdoptions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({user_id: user.user_id}),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch adoptions');
      }

      const data = await response.json();
      setAdoptions(data.adoptions || []);
      setLoading(false);
    } catch (err) {
      setError('An error occurred while fetching adoptions');
      setLoading(false);
    }
  };

  if (loading) return <Loader message="Fetching Adoptions..."/>;
  if (error) return <div>{error}</div>;

  return (
    <>
      <AdminNavBar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Manage Adoptions</h1>
        {loading && <Loader message="Fetching Adoptions..." />}
        {error && <p className="text-red-500 mb-4 bg-red-100 p-3 rounded">{error}</p>}
        {!loading && !error && (
          <>
            {adoptions.length === 0 ? (
              <p className="text-gray-600 text-lg">No adoptions found.</p>
            ) : (
              <div className="bg-white shadow-md rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Adoption Date</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pet</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Adopter</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {adoptions.map((adoption) => (
                      <tr key={adoption.adoption_id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{adoption.adoption_id}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(adoption.adoption_date).toLocaleDateString()}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{adoption.pet_name}</div>
                          <div className="text-sm text-gray-500">{adoption.pet_type} - {adoption.pet_breed}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{adoption.adopter_name}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                            ${adoption.application_status === 'approved' ? 'bg-green-100 text-green-800' : 
                              adoption.application_status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                              'bg-red-100 text-red-800'}`}>
                            {adoption.application_status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
}

export default AdminManageAdoptionsPage;