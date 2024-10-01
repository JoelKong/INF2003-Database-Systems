import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AdminNavBar from "./AdminNavbar.tsx";
import Loader from "../general/Loader.tsx";

function AdminPetApplicationPage() {
  const [application, setApplication] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState(null);
  const { application_id } = useParams();

  useEffect(() => {
    fetchApplicationDetail();
  }, [application_id]);

  const fetchApplicationDetail = async () => {
    try {
      setLoading(true);
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/getApplications/${application_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: user.user_id }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch application details');
      }

      const data = await response.json();
      if (data.status === 'success') {
        setApplication(data.application);
        setStatus(data.application.status);
      } else {
        throw new Error(data.message || 'Failed to fetch application details');
      }
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = (e) => {
    setStatus(e.target.value);
  };

  const handleSubmit = async () => {
    if (status === 'approved') {
      if (!window.confirm('Are you sure you want to approve this application? This will create an adoption record.')) {
        return;
      }
    }

    setIsUpdating(true);
    try {
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/updateApplicationStatus/${application_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status, user_id: user.user_id, pet_id: application.pet_id }),
      });

      const data = await response.json();

      if (response.ok && data.status === 'success') {
        alert(data.message);
        await fetchApplicationDetail();
      } else {
        throw new Error(data.message || 'Failed to update status');
      }
    } catch (error) {
      console.error('Error updating status:', error);
      alert(error.message || 'An error occurred while updating status');
    } finally {
      setIsUpdating(false);
    }
  };

  if (loading) return <Loader message="Fetching Application Details..." />
  if (error) return <div className="text-center mt-8 text-red-500">Error: {error}</div>;
  if (!application) return <div className="text-center mt-8">No application found</div>;

  return (
    <>
      <AdminNavBar />

      <main className="flex justify-center items-center min-h-screen bg-gray-100 p-4">
        <div className="bg-white shadow-xl rounded-lg overflow-hidden max-w-2xl w-full">
          <div className="p-4 sm:p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Application Details</h1>

            <img
              src={application.pet_image}
              alt={application.pet_name}
              className="w-full h-64 object-cover rounded-lg mb-4"
            />

            <div className="grid grid-cols-2 gap-4">
              <p className="text-sm text-gray-600">Application ID:</p>
              <p className="text-sm font-semibold">{application.application_id}</p>

              <p className="text-sm text-gray-600">Applicant Username:</p>
              <p className="text-sm font-semibold">{application.applicant_username}</p>

              <p className="text-sm text-gray-600">Pet Name:</p>
              <p className="text-sm font-semibold">{application.pet_name}</p>

              <p className="text-sm text-gray-600">Type:</p>
              <p className="text-sm font-semibold">{application.pet_type}</p>

              <p className="text-sm text-gray-600">Breed:</p>
              <p className="text-sm font-semibold">{application.breed}</p>

              <p className="text-sm text-gray-600">Gender:</p>
              <p className="text-sm font-semibold">{application.gender}</p>

              <p className="text-sm text-gray-600">Age:</p>
              <p className="text-sm font-semibold">{application.age_month} months</p>

              <p className="text-sm text-gray-600">Submission Date:</p>
              <p className="text-sm font-semibold">
                {new Date(application.submission_date).toLocaleDateString()}
              </p>

              <p className="text-sm text-gray-600">Status:</p>
              <div className="flex items-center">
                <select
                  value={status}
                  onChange={handleStatusChange}
                  className="text-sm font-semibold bg-white border border-gray-300 rounded px-2 py-1"
                  disabled={isUpdating}
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
                <button
                  onClick={handleSubmit}
                  className={`ml-2 ${isUpdating ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'} text-white px-3 py-1 rounded text-sm`}
                  disabled={isUpdating}
                >
                  {isUpdating ? 'Updating...' : 'Update Status'}
                </button>
              </div>
            </div>

            <div className="mt-4">
              <p className="text-sm text-gray-600">Description:</p>
              <p className="text-sm mt-1">{application.pet_description}</p>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}

export default AdminPetApplicationPage;