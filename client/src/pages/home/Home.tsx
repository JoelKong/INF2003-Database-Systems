import NavBar from "../general/NavBar";
import Landing from "./components/Landing";

export default function Home(): JSX.Element {
  return (
    <div className="w-screen h-screen">
      <NavBar />
      <Landing />
    </div>
  );
}
