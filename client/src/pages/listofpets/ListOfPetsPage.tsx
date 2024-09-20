import NavBar from "../general/NavBar";
import Pets from "./components/Pets";

export default function ListOfPetsPage(): JSX.Element {
  return (
    <div className="h-screen w-screen">
      <NavBar />
      <Pets />
    </div>
  );
}
