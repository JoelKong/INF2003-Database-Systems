import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home/Home";
import ListOfPets from "./pages/listofpets/ListOfPets";

function App() {
  return (
    <>
      <div className="fixed h-screen w-screen bg-home-bg bg-contain bg-center z-10"></div>
      <main className="relative z-20">
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/listofpets" element={<ListOfPets />} />
            {/* <Route path="/path2" element={<component2 />} />
          <Route exact path="/path3" element={<component3 />} /> */}
          </Routes>
        </Router>
      </main>
    </>
  );
}

export default App;
