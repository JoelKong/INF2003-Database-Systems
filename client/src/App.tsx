/** @format */

import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import HomePage from "./pages/home/HomePage";
import ListOfPetsPage from "./pages/listofpets/ListOfPetsPage.tsx";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import FavouritesPage from "./pages/favourites/FavouritesPage.tsx";
import Cart from "./pages/cart/Cart.tsx";
import Checkout from "./pages/checkout/Checkout.tsx";
import AdminRegisterPage from "./pages/admin_register/AdminRegisterPage.tsx";

function App() {
  return (
    <>
      <div className="fixed h-screen w-screen bg-home-bg bg-contain bg-center z-10"></div>
      <main className="relative z-20">
        <Router>
          <Routes>
            <Route path="/" element={<HomePage/>}/>
            <Route path="/login" element={<LoginPage/>}/>
            <Route path="/register" element={<RegisterPage/>}/>
            <Route path="/listofpets" element={<ListOfPetsPage/>}/>
            <Route path="/favourites" element={<FavouritesPage/>}/>
            <Route path="/cart" element={<Cart/>}/>
            <Route path="/checkout" element={<Checkout/>}/>
            <Route path="/adminregister" element={<AdminRegisterPage />} />
          </Routes>
        </Router>
      </main>
    </>
  );
}


export default App;
