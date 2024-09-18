import NavBar from "../general/NavBar";

export default function Favourites(): JSX.Element {
  return (
    <div className="h-screen w-screen">
      <NavBar />
      <div className="pt-16">
        {/* Add content here */}
        <h1 className="text-2xl">Favourite Page</h1>
      </div>
    </div>
  );
}
