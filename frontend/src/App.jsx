import { useState , useEffect } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import {ChooseTeam} from "./pages/ChooseTeam/ChooseTeam.jsx";
import {TeamPage} from "./pages/TeamPage/TeamPage.jsx";
function App() {
    const [teams,setTeams]=useState([])
    useEffect(()=>{
        fetchTeams()
    },[])
    const fetchTeams = async ()=>{
        const response = await fetch("http://127.0.0.1:5000/api/teams/")
        const data = await response.json()
        setTeams(data.teams)
    }
    return (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<ChooseTeam teams={teams}/>} />
            <Route path="/teams/:team_name" element={<TeamPage/>}></Route>  
          </Routes>
        </BrowserRouter>
    )
}

export default App
