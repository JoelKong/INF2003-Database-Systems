import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/home/Home";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* <Route path="/path2" element={<component2 />} />
        <Route exact path="/path3" element={<component3 />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
