import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import PetCard from "../../listofpets/components/PetCard";

export default function Landing(): JSX.Element {
  const navigate = useNavigate();
  const [topPets, setTopPets] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTopPets() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/getTop3`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        setTopPets(data);
      } catch (error) {
        console.error("Error fetching top pets:", error);
        setError("Failed to fetch top pets. Please try again later.");
      }
    }

    fetchTopPets();
  }, []);

  return (
    <div className="w-full h-full flex flex-col items-center mt-12">
      <div className="w-full max-w-3xl bg-gradient-to-tr from-amber-600 to-orange-300 rounded-lg shadow-lg p-10 mb-8 text-center">
        <h1 className="tracking-wide font-bold text-4xl text-gray-700 mb-6">
          Adopt A Pet Today!
        </h1>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
          onClick={() => navigate("/listofpets")}
        >
          Adopt Now
        </button>
      </div>

      <div className="bg-white border border-gray-300 rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-semibold text-gray-800 mb-6 text-center">
          Top 3 Favourite Pets
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {topPets.map((pet) => (
            <PetCard key={pet.pet_id} petDetails={pet} />
          ))}
        </div>
      </div>
    </div>
  );
}
