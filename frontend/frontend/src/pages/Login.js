import { useNavigate } from "react-router-dom";

function Login({ setUsuario }) {
  const [ci, setCi] = useState("");
  const [rol, setRol] = useState("votante");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ci, rol })
    });

    const data = await res.json();

    if (data.ok) {
      setUsuario(data.usuario); // guarda el usuario
      if (rol === "votante") {
        navigate("/votante");
      } else {
        navigate("/mesa");
      }
    } else {
      alert("Login fallido");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* CI y rol como antes */}
    </form>
  );
}
