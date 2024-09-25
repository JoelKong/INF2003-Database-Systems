import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AdminNavBar from "./AdminNavbar";

function AdminPage() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = sessionStorage.getItem("user");

    if (user) {
      setUser(JSON.parse(user));
    } else {
      navigate("/admin/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    sessionStorage.removeItem("user");
    navigate("/admin/login");
  };

  if (!user) return null;

  return <AdminNavBar />;
}

export default AdminPage;
