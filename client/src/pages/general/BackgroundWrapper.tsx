import {useLocation} from "react-router-dom";

function BackgroundWrapper({ children }) {
  const location = useLocation();
  const isAdminPage = location.pathname.startsWith('/admin') || location.pathname === '/adminregister';

  return (
    <>
      {!isAdminPage && (
        <div className="fixed h-screen w-screen bg-home-bg bg-contain bg-center z-10"></div>
      )}
      <main className="relative z-20">
        {children}
      </main>
    </>
  );
}

export default BackgroundWrapper;