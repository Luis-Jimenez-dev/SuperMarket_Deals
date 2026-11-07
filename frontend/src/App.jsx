import './App.css'
import { Routes, Route } from 'react-router-dom'

import HomePage from './pages/HomePage'
import DealsPage from './pages/DealsPage'
import MealPlanPage from './pages/MealPlanPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/deals" element={<DealsPage />} />
      <Route path="/meal-plan" element={<MealPlanPage />} />

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App