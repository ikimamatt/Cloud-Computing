import React, { useState, useEffect } from 'react';

function App() {
  // State untuk menyimpan data yang diambil dari API
  const [apiData, setApiData] = useState(null);

  // useEffect digunakan untuk melakukan side effect, yaitu fetching data dari API saat komponen pertama kali di-render
  useEffect(() => {
    console.log('Fetching data...'); // Menampilkan pesan di console saat fetching data dimulai

    fetch('http://localhost:5000/api/data') // Mengambil data dari API Flask yang berjalan di localhost:5000
      .then(response => {
        if (!response.ok) { // Jika response tidak OK (misalnya error 404 atau 500)
          throw new Error('Network response was not ok'); // Melempar error agar bisa ditangkap di catch
        }
        return response.json(); // Mengonversi response menjadi JSON
      })
      .then(data => {
        console.log(data); // Menampilkan data yang diterima di console
        setApiData(data.data); // Menyimpan data ke state agar bisa ditampilkan di UI
      })
      .catch(error => console.error('Fetch error:', error)); // Menangani error jika terjadi kesalahan dalam fetching data
  }, []); // Dependency array kosong berarti useEffect hanya dijalankan sekali saat komponen pertama kali dimount

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>React & Flask Integration</h1>
      {/* Menampilkan data dari API, jika belum ada maka tampilkan "Loading data..." */}
      <p>{apiData ? apiData : "Loading data..."}</p>
    </div>
  );
}

export default App;
