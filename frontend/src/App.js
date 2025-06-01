import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Layout/Navbar';
import Login from './components/Auth/Login';
import VehiculoList from './components/Vehiculos/VehiculoList';
import Register from './components/Auth/Register';

// Crear un tema personalizado
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<div>Página de Inicio</div>} />
            <Route path="/login" element={<Login />} />
            <Route path="/vehiculos" element={<VehiculoList />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
