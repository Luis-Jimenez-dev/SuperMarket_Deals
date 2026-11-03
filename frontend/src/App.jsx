import './App.css'
import HomePage from './pages/HomePage'
import DealsPage from './pages/DealsPage'
import MealPlanPage from './pages/MealPlanPage'
import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/deals" element={<DealsPage />} />
      <Route path="/meal-plan" element={<MealPlanPage />} />
    </Routes>
  )
}

export default App