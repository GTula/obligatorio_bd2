export async function loginVotante({ serie, numero }) {
  return await fetch("http://127.0.0.1:5000/api/login_votante", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ serie, numero })
  });
}
