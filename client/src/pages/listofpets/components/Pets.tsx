import { IoMdArrowDropdown } from "react-icons/io";
import { useState, useEffect } from "react";
import PetCard from "./PetCard";

export default function Pets(): JSX.Element {
  const [pets, setPets] = useState<any>([]);
  const [searchedValue, setSearchedValue] = useState<any>({
    value: "",
    type: "name",
  });
  const [toggleSearchType, setToggleSearchType] = useState<boolean>(false);
  const [dummyPet, setDummyPet] = useState<any>({
    pet_id: 1,
    pet_name: "Yuki",
    pet_type: "Dog",
    breed: "Samoyed",
    age_month: "1",
    pet_description:
      "Yuki is a cutie patotidddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddde",
    image:
      "data:image/jpeg;base64,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",
  });

  function changeSearchType(type: string) {
    setSearchedValue({ value: "", type: type });
    setToggleSearchType(false);
  }

  async function getPets() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/getpets");
      const data = await response.json();
      setPets(data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    }
  }

  async function filterPets(e: any) {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/filterpets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(searchedValue),
      });

      const data = await response.json();
      setPets(data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    }
  }

  useEffect(() => {
    getPets();
  }, []);

  return (
    <section className="w-screen h-screen flex justify-center items-center text-gray-700">
      <div className="w-11/12 border-2 h-4/5 bg-white rounded-lg flex flex-col items-center p-4">
        <div className="flex flex-row w-full items-center justify-center relative">
          <h1 className="font-bold text-2xl border-b-4 border-gray-700 text-center">
            List Of Pets
          </h1>
          <div className="w-26 border-2 rounded-lg border-gray-600 flex flex-row absolute right-0">
            <form onSubmit={(e: any) => filterPets(e)}>
              <input
                className="w-full p-2 tracking-widest rounded-lg outline-none"
                placeholder={`Search for ${searchedValue.type}`}
                value={searchedValue.value}
                onChange={(e: any) => {
                  setSearchedValue({ ...searchedValue, value: e.target.value });
                }}
              />
            </form>
            <button
              className="w-1/6 flex justify-center items-center border-l-2 border-black"
              onClick={() => {
                setToggleSearchType(!toggleSearchType);
              }}
            >
              <IoMdArrowDropdown />
            </button>
            {toggleSearchType && (
              <div className="absolute top-full w-full bg-white border-gray-600 border-2 mt-[0.01rem] rounded-br-md rounded-bl-md">
                <button
                  className="p-2 w-full border-b-2 text-left tracking-widest"
                  onClick={() => {
                    changeSearchType("name");
                  }}
                >
                  Search for name
                </button>
                <button
                  className="p-2 w-full border-b-2 text-left tracking-widest"
                  onClick={() => {
                    changeSearchType("type");
                  }}
                >
                  Search for type
                </button>
                <button
                  className="p-2 w-full border-b-2 text-left tracking-widest"
                  onClick={() => {
                    changeSearchType("breed");
                  }}
                >
                  Search for breed
                </button>
              </div>
            )}
          </div>
        </div>
        <div className="w-full mt-4 pl-6 pr-6 h-full flex flex-row flex-wrap justify-evenly overflow-y-scroll overflow-x-hidden">
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          <PetCard petDetails={dummyPet} />
          {pets.map((pet: any, index: any) => {
            <PetCard petDetails={pet} key={index} />;
          })}
        </div>
      </div>
    </section>
  );
}
