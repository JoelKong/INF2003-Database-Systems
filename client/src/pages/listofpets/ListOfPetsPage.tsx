import NavBar from "../general/NavBar";
import Pets from "./components/Pets";
import {useEffect, useState} from "react";

export default function ListOfPetsPage(): JSX.Element {
  const [petsData, setPetsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/getpets',
          {credentials: "include"}
          );
        const data = await response.json();
        setPetsData(data);
      } catch (error) {
        console.error("Error fetching pets data: ", error)
      }
    }

    fetchData();
  }, [])

  console.log(petsData)

  return (
    <div className="h-screen w-screen">
      <NavBar />
      <Pets />
    </div>
  );
}
