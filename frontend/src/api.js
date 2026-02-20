import axios from "axios";

const BACKEND_URL = "https://fintrace-ai.onrender.com";

export async function analyzeCSV(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(
    `${BACKEND_URL}/analyze`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  );

  return response.data;
}
