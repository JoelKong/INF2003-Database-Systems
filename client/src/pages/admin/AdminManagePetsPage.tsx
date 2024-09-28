import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Loader from "../general/Loader";
import AdminNavBar from "./AdminNavbar";
import PetCardAdmin from "./PetCardAdmin";

export default function AdminManagePetsPage() {
  const navigate = useNavigate();
  const [pets, setPets] = useState<any>([])
  const [loading, setLoading] = useState(true);
  const [togglePetConditions, setTogglePetConditions] = useState<any>({
    toggle: false,
    data: {},
  });


  async function getPets() {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/getpets");
      const data = await response.json();
      setPets(data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      const parsedUser = JSON.parse(user);
      if (parsedUser.role !== "admin") {
        navigate("/")
      }
    }

    getPets()
  }, []);


  return (
    <>
      <AdminNavBar/>
      <section className="w-screen h-screen flex justify-center items-center text-gray-700 overflow-x-hidden">
      {loading && <Loader message="Fetching pets..." />}

      {togglePetConditions.toggle && (
        <section className="w-screen h-screen fixed flex justify-center items-center backdrop-blur-sm z-50">
          <div className="h-5/6 shadow-2xl rounded-lg bg-white">
            <div className="h-3/6 border-b-2">
              <img
                className="w-full h-full object-contain"
                src={togglePetConditions.data.image}
                alt={togglePetConditions.data.name}
              />
            </div>
            <div className="flex flex-col h-3/6 justify-evenly p-4 tracking-wide overflow-y-auto overflow-x-hidden break-words">
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
                onClick={() =>
                  setTogglePetConditions({ toggle: false, data: {} })
                }
              >
                Back
              </button>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Weight: </p>
                {togglePetConditions.data.weight}
              </div>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Vaccination Date: </p>
                {togglePetConditions.data.vaccination_date}
              </div>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Health Condition: </p>
                {togglePetConditions.data.health_condition}
              </div>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Sterilisation Status: </p>
                {togglePetConditions.data.sterilisation_status}
              </div>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Adoption Fee: </p>
                {togglePetConditions.data.adoption_fee}
              </div>
              <div className="flex flex-row mb-2">
                <p className="font-bold mr-1">Previous Owner: </p>
                {togglePetConditions.data.previous_owner}
              </div>
            </div>
          </div>
        </section>
      )}
      <div className="w-11/12 border-2 h-4/5 bg-white rounded-lg flex flex-col items-center p-4">
        <div className="flex flex-row w-full items-center justify-center relative">
          <h1 className="font-bold text-2xl border-b-4 border-gray-700 text-center">
            Manage Pets
          </h1>
        </div>
        <div
          className="w-full mt-4 pl-6 pr-6 h-full flex flex-row flex-wrap justify-evenly overflow-y-scroll overflow-x-hidden"
        >
          {pets.length > 0 ? (
            pets.map((pet: any) => {
              return (
                <PetCardAdmin
                  petDetails={pet}
                  setTogglePetConditions={setTogglePetConditions}
                  setPets={setPets}
                  pets={pets}
                  key={pet.pet_id}
                />
              );
            })
          ) : (
            <div className="w-full h-full text-center text-xl font-bold">
              No Pets Available
            </div>
          )}
        </div>
      </div>
    </section>
    </>
  )
}
