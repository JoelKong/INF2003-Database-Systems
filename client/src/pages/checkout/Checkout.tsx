import { useLocation, useNavigate } from "react-router-dom";
import NavBar from "../general/NavBar";

export default function Checkout(): JSX.Element {
  const location = useLocation();
  const { cart } = location.state || { cart: [] };
  const navigate = useNavigate();

  async function confirmReservation(e: any) {
    e.preventDefault();
    const user: any = sessionStorage.getItem("user");
    const adopter_id = JSON.parse(user).adopter_id;
    const response = await fetch(
      "http://127.0.0.1:5000/api/v1/confirmreservation",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          adopter_id: adopter_id,
          cart: cart,
        }),
      }
    );

    await response.json();
    alert("Successfully reserved pets in cart!");
    navigate("/listofpets");
  }

  return (
    <div className="h-screen w-screen">
      <NavBar />
      <section className="w-screen h-screen flex justify-center items-center text-gray-700">
        <div className="w-11/12 border-2 h-4/5 bg-white rounded-lg flex flex-col items-center p-4">
          <div className="flex flex-row w-full items-center justify-center relative">
            <h1 className="font-bold text-2xl border-b-4 border-gray-700 text-center">
              Confirm Reservation
            </h1>
          </div>
          <div className="w-full mt-4 pl-6 pr-6 h-full flex flex-row flex-wrap justify-center items-center overflow-y-scroll overflow-x-hidden">
            <form
              className="w-1/2 h-full border-2 rounded-lg bg-gray-300 flex justify-evenly items-center flex-col"
              onSubmit={(e: any) => {
                confirmReservation(e);
              }}
            >
              After booking, please come to our center for further instructions
              <div>
                Email: <input />
              </div>
              <div>
                Name: <input />
              </div>
              <div>
                Phone Number: <input />
              </div>
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
                onClick={(e: any) => {
                  confirmReservation(e);
                }}
              >
                Confirm Reservation
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
}
