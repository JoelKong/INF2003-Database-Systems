import React, { useState, useEffect } from 'react';
import AdminNavBar from "./AdminNavbar";

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
        body: JSON.stringify({ admin_id: adminUser.user_id }),
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

  if (loading) return <p>Loading applications...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <>
      <AdminNavBar />
      <div className="container mx-auto mt-8">
        <h1 className="text-2xl font-bold mb-4">Adoption Applications</h1>
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Application ID</th>
              <th className="py-2 px-4 border-b">User</th>
              <th className="py-2 px-4 border-b">Pet</th>
              <th className="py-2 px-4 border-b">Submission Date</th>
              <th className="py-2 px-4 border-b">Status</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((app) => (
              <tr key={app.application_id}>
                <td className="py-2 px-4 border-b">{app.application_id}</td>
                <td className="py-2 px-4 border-b">{app.username}</td>
                <td className="py-2 px-4 border-b">{app.pet_name}</td>
                <td className="py-2 px-4 border-b">{new Date(app.submission_date).toLocaleDateString()}</td>
                <td className="py-2 px-4 border-b">{app.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default AdminApplicationsPage;