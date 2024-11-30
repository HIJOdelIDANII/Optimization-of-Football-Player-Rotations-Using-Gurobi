import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import {ChooseTeam} from "./pages/ChooseTeam/ChooseTeam.jsx";
function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChooseTeam/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
