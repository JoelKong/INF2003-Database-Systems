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
  const [editPetToggle, setEditPetToggle] = useState<any>({
    toggle: false,
    data: {},
  })


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

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setEditPetToggle((prevState: any) => ({
      ...prevState,
      data: {
        ...prevState.data,
        [name]: value,
      },
    }));
  };

  async function editPet(e: any, petData: any) {
    e.preventDefault()

    const userSession: any = sessionStorage.getItem("user")
    const user = JSON.parse(userSession);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/v1/admin/editPet",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ pet_data: petData, user_id: user.adopter_id }),
        }
      );

      if (response.status === 200) {
        const updatedPets = pets.map((pet: any) => 
          pet.pet_id === editPetToggle.data.pet_id ? editPetToggle.data : pet
        );
        setPets(updatedPets);
        alert(`${editPetToggle.data.name} has been updated.`);

      } else {
        const data = await response.json();
        alert(data.error || "Failed to update.");
      }
    } catch (error) {
      console.error("Error updating pet:", error);
      alert("An error occurred while updating pet.");
    }

    setEditPetToggle((prevState: any) => ({
      ...prevState,
      toggle: false
    }))
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
      <section className="w-full h-screen flex justify-center items-center text-gray-700 overflow-x-hidden">
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

      {editPetToggle.toggle && <section className="w-screen h-screen fixed flex justify-center items-center backdrop-blur-sm z-50">
          <div className="h-5/6 w-5/6 shadow-2xl rounded-lg bg-white">
            <div className="h-3/6 border-b-2">
              <img
                className="w-full h-full object-contain"
                src={editPetToggle.data.image}
                alt={editPetToggle.data.name}
              />
            </div>
            <div className="flex flex-col h-3/6 justify-evenly p-4 tracking-wide overflow-y-auto overflow-x-hidden break-words">
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
                onClick={() =>
                  setEditPetToggle({
                    toggle: false,
                    data: {},
                  })
                }
              >
                Back
              </button>
              <form onSubmit={(e: any) => {editPet(e, editPetToggle.data)}} className="mt-2 mb-2">
              <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Name: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="name" value={editPetToggle.data.name} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Type: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="type" value={editPetToggle.data.type} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Breed: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="breed" value={editPetToggle.data.breed} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Gender: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="gender" value={editPetToggle.data.gender} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Age: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="age_month" value={editPetToggle.data.age_month} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Description: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="description" value={editPetToggle.data.description} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Weight: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="weight" value={editPetToggle.data.weight} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Vaccination Date: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="vaccination_date" value={editPetToggle.data.vaccination_date} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Health Condition: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="health_condition" value={editPetToggle.data.health_condition} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Sterilisation Status: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="status" value={editPetToggle.data.sterilisation_status} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Adoption Fee: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="adoption_fee" value={editPetToggle.data.adoption_fee} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
                <div className="flex flex-row mb-2">
                  <p className="font-bold mr-1">Previous Owner: </p>
                  <input className="border-2 rounded-lg pl-2 pr-2 border-black tracking-wide" name="previous_owner" value={editPetToggle.data.previous_owner} onChange={(e: any) => {handleInputChange(e)}}/>
                </div>
              </form>
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
                onClick={(e: any) =>
                  editPet(e, editPetToggle.data)
                }
              >
                Update Pet
              </button>
            </div>
          </div>
        </section>}
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
                  setEditPetToggle={setEditPetToggle}
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

