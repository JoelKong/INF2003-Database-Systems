import {useState, useEffect} from 'react';
import AdminNavBar from "./AdminNavbar";
import Loader from "../general/Loader.tsx";

interface Application {
  application_id: number;
  user_id: number;
  pet_id: number;
  submission_date: string;
  status: string;
  username: string;
  pet_name: string;
}

function AdminApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const adminUser = JSON.parse(sessionStorage.getItem('user') || '{}');
      const response = await fetch('http://127.0.0.1:5000/api/v1/admin/getApplications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({admin_id: adminUser.user_id}),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch applications');
      }

      const data = await response.json();
      setApplications(data.applications);
    } catch (err) {
      setError('Error fetching applications');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader message="Fetching Applications..."/>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <>
      <AdminNavBar/>

      {loading && <Loader message="Fetching application details..." />}

      <div className="container mx-auto mt-8">
        <h1 className="text-2xl font-bold mb-4">Adoption Applications</h1>

        <div className="overflow-x-auto shadow-md sm:rounded-lg">
          <table className="w-full text-sm text-left text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3">Application ID</th>
              <th scope="col" className="px-6 py-3">User</th>
              <th scope="col" className="px-6 py-3">Pet</th>
              <th scope="col" className="px-6 py-3">Submission Date</th>
              <th scope="col" className="px-6 py-3">Status</th>
            </tr>
            </thead>
            <tbody>
            {applications.map((app, index) => (
              <tr key={app.application_id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">{app.application_id}</td>
                <td className="px-6 py-4">{app.username}</td>
                <td className="px-6 py-4">{app.pet_name}</td>
                <td className="px-6 py-4">{new Date(app.submission_date).toLocaleDateString()}</td>
                <td className="px-6 py-4">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              app.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                app.status === 'approved' ? 'bg-green-100 text-green-800' :
                  'bg-red-100 text-red-800'
            }`}>
              {app.status}
            </span>
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default AdminApplicationsPage;