/** @format */

import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import HomePage from "./pages/home/HomePage";
import ListOfPetsPage from "./pages/listofpets/ListOfPetsPage.tsx";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import FavouritesPage from "./pages/favourites/FavouritesPage.tsx";
import Cart from "./pages/cart/Cart.tsx";
import Checkout from "./pages/checkout/Checkout.tsx";
import AdminLoginPage from "./pages/admin_login/AdminLoginPage.tsx";
import AdminManagePetsPage from "./pages/admin/AdminManagePetsPage.tsx";
import AdminRegisterPage from "./pages/admin_register/AdminRegisterPage.tsx";
import BackgroundWrapper from "./pages/general/BackgroundWrapper.tsx";
import AdminManageUsersPage from "./pages/admin/AdminManageUsersPage.tsx";
import AdminAddUserPage from "./pages/admin/AdminAddUserPage.tsx";
import AdminManageUserPage from "./pages/admin/AdminManageUserPage.tsx";
import AdminApplicationsPage from "./pages/admin/AdminApplicationsPage.tsx";
import AdminPetApplicationPage from "./pages/admin/AdminPetApplicationPage.tsx";
import AdminManageAdoptions from "./pages/admin/AdminManageAdoptions.tsx";

function App() {
  return (
    <>
      <Router>
        <BackgroundWrapper>
          <Routes>
            <Route path="/" element={<HomePage/>}/>
            <Route path="/login" element={<LoginPage/>}/>
            <Route path="/register" element={<RegisterPage/>}/>
            <Route path="/listofpets" element={<ListOfPetsPage/>}/>
            <Route path="/favourites" element={<FavouritesPage/>}/>
            <Route path="/cart" element={<Cart/>}/>
            <Route path="/checkout" element={<Checkout/>}/>
            <Route path="/adminregister" element={<AdminRegisterPage/>}/>
            <Route path="/admin/login" element={<AdminLoginPage/>}/>
            <Route path="/admin/managepets" element={<AdminManagePetsPage/>}/>
            <Route path="/admin/manage-users" element={<AdminManageUsersPage/>} />
            <Route path="/admin/add-user" element={<AdminAddUserPage/>} />
            <Route path="/admin/manage-user/:user_id" element={<AdminManageUserPage />} />
            <Route path="/admin/applications" element={<AdminApplicationsPage />} />
            <Route path="/admin/applications/:application_id" element={<AdminPetApplicationPage />} />
            <Route path="/admin/manage-adoptions" element={<AdminManageAdoptions />} />
          </Routes>
        </BackgroundWrapper>
      </Router>
    </>
  );
}


export default App;
